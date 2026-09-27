#!/usr/bin/env python3
"""
Download the @fontsource/<name> npm packages listed in
fontsource_families.yaml directly from the npm registry (no npm/node
needed — pure tarball fetch), extracting each into manual/fontsource/<name>/
ready for pipeline.py.

Usage:
    python3 scripts/fetch_fontsource_families.py
    (reads fontsource_families.yaml in the repo root, writes into
    manual/fontsource/)
"""
import argparse
import io
import json
import shutil
import sys
import tarfile
import urllib.request
from pathlib import Path

import manifest_lib

REGISTRY = "https://registry.npmjs.org/@fontsource"
FAMILIES_FILE = Path("fontsource_families.yaml")
OUT_DIR = Path("manual/fontsource")


def fetch_json(url):
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def fetch_package(name: str, out_dir: Path):
    meta = fetch_json(f"{REGISTRY}/{name}")
    latest = meta["dist-tags"]["latest"]
    tarball_url = meta["versions"][latest]["dist"]["tarball"]
    with urllib.request.urlopen(tarball_url) as resp:
        data = resp.read()

    dest = out_dir / name
    if dest.exists():
        shutil.rmtree(dest)
    dest.mkdir(parents=True, exist_ok=True)

    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        for member in tar.getmembers():
            # npm tarballs nest everything under a leading "package/" dir
            parts = Path(member.name).parts
            if not parts or parts[0] != "package" or len(parts) < 2:
                continue
            member.name = str(Path(*parts[1:]))
            tar.extract(member, path=dest)
    return latest


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--production-manifest-url", default=manifest_lib.DEFAULT_MANIFEST_URL)
    ap.add_argument("--force", nargs="*", default=[],
                     help="Package name(s) to re-fetch even though already published (e.g. 'inter'), "
                          "or 'all' to fetch everything listed in fontsource_families.yaml.")
    args = ap.parse_args()

    if not FAMILIES_FILE.exists():
        print(f"No {FAMILIES_FILE} found — nothing to fetch from Fontsource. "
              f"(This is fine if you're not using fontsource sources.)")
        return

    all_names = []
    for line in FAMILIES_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line == "families:":
            continue
        all_names.append(line)
    if not all_names:
        print(f"{FAMILIES_FILE} has no families listed — skipping fontsource fetch.")
        return

    published = manifest_lib.published_sources(manifest_lib.load_production_manifest(args.production_manifest_url))
    force = set(args.force)
    if "all" in force:
        names = all_names
    else:
        names = [n for n in all_names if f"{OUT_DIR.as_posix()}/{n}" not in published or n in force]
    skipped = len(all_names) - len(names)
    if skipped:
        print(f"Skipping {skipped} already-published packages (pass --force <name> to re-fetch one, "
              f"or --force all to re-fetch everything)")
    if not names:
        print("Nothing new to fetch from Fontsource — every listed package is already published.")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Fetching {len(names)} families from Fontsource (npm registry)...")

    missing = []
    for name in names:
        try:
            version = fetch_package(name, OUT_DIR)
            print(f"  OK {name} @ {version}")
        except Exception as e:
            print(f"  FAILED {name}: {e}", file=sys.stderr)
            missing.append(name)

    found = len(names) - len(missing)
    print(f"Fetched {found}/{len(names)} requested families into {OUT_DIR}")
    if missing:
        print("WARNING: these entries failed to fetch (check the exact npm "
              "name, e.g. 'inter' not '@fontsource/inter'):", file=sys.stderr)
        for m in missing:
            print(f"  - {m}", file=sys.stderr)


if __name__ == "__main__":
    main()
