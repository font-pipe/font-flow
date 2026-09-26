#!/usr/bin/env python3
"""
Sparse-checkout only the families listed in families.yaml from google/fonts.

This intentionally does NOT do a full clone — google/fonts is tens of GB
across its history. --filter=blob:none --depth=1 plus a cone sparse-checkout
pulls only the requested family folders, in seconds, regardless of how many
families are requested or how large the full repo is.

Verified against a real mixed ofl/ + apache/ request (see conversation this
was built from) — sparse-checkout handles multiple license directories in a
single pass correctly.

Usage:
    python3 scripts/fetch_google_families.py
    (reads families.yaml in the repo root, writes into .cache/gfonts/)
"""
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/google/fonts.git"
CLONE_DIR = Path(".cache/gfonts")
FAMILIES_FILE = Path("families.yaml")


def main():
    if not FAMILIES_FILE.exists():
        print(f"No {FAMILIES_FILE} found — nothing to fetch from google/fonts. "
              f"(This is fine if you're only using manual/ sources.)")
        return

    families = []
    for line in FAMILIES_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line == "families:":
            continue
        families.append(line)
    if not families:
        print(f"{FAMILIES_FILE} has no families listed — skipping google/fonts fetch.")
        return

    if CLONE_DIR.exists():
        shutil.rmtree(CLONE_DIR)
    CLONE_DIR.parent.mkdir(parents=True, exist_ok=True)

    print(f"Fetching {len(families)} families from google/fonts (sparse, shallow)...")
    subprocess.run(
        ["git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1", REPO_URL, str(CLONE_DIR)],
        check=True,
    )
    subprocess.run(["git", "sparse-checkout", "init", "--cone"], cwd=CLONE_DIR, check=True)
    subprocess.run(["git", "sparse-checkout", "set", *families], cwd=CLONE_DIR, check=True)
    subprocess.run(["git", "checkout", "main"], cwd=CLONE_DIR, check=True)

    # Sanity check: warn (don't fail) about any requested family that didn't
    # actually materialize — usually means a typo'd path in families.yaml.
    missing = [f for f in families if not (CLONE_DIR / f).is_dir()]
    if missing:
        print(f"WARNING: these entries in families.yaml produced no directory "
              f"(check the path is exactly right, e.g. 'ofl/oswald'):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)

    found = len(families) - len(missing)
    print(f"Fetched {found}/{len(families)} requested families into {CLONE_DIR}")

    # A handful of typo'd paths is normal and shouldn't block the build.
    # Losing the vast majority is not normal — that's a sign the clone or
    # sparse-checkout itself went wrong (bad branch name, git behavior
    # change, network issue, etc.), and silently continuing here is exactly
    # what let a near-empty google/fonts fetch flow all the way through to
    # a deployed manifest before.
    if families and found < len(families) * 0.9:
        print(
            f"FATAL: only {found}/{len(families)} requested families were fetched — "
            f"too many missing to be normal typos. Aborting instead of continuing "
            f"with a near-empty google/fonts source.",
            file=sys.stderr,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
