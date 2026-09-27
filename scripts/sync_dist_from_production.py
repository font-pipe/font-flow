#!/usr/bin/env python3
"""
Cloudflare Pages deployments are full snapshots: whatever's in dist/ at
deploy time becomes the complete live site, and anything missing gets
dropped. Since we no longer keep old font files in git or in a GitHub
Actions cache, this script re-downloads every file for every family
that's ALREADY live (i.e. not one of the families pipeline.py just built
fresh this run) straight from the live site, so dist/ ends up complete
again before deploy.

If you switch deployment to R2 with `aws s3 sync` (no --delete), you
don't need this script at all — sync only touches new/changed files and
leaves everything already in the bucket alone. See the commented R2
block in build-and-deploy.yml.

Usage:
    python3 scripts/sync_dist_from_production.py <production_base_url> dist/manifest.json dist/
"""
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import urllib.request

MAX_WORKERS = 16


def download(base_url: str, rel_path: str, out_root: Path):
    dest = out_root / rel_path
    if dest.exists():
        return  # already have it locally (this run just built it)
    dest.parent.mkdir(parents=True, exist_ok=True)
    url = f"{base_url.rstrip('/')}/{rel_path}"
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; font-flow-sync/1.0)"})
    with urllib.request.urlopen(request) as resp:
        dest.write_bytes(resp.read())


def main():
    if len(sys.argv) != 4:
        print("Usage: sync_dist_from_production.py <base_url> <manifest_path> <dist_dir>", file=sys.stderr)
        sys.exit(2)

    base_url, manifest_path, dist_dir = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3])
    entries = json.loads(manifest_path.read_text()).get("fonts", [])

    to_fetch = []
    for entry in entries:
        for f in entry.get("files", []):
            to_fetch.append(f["path"])
        if entry.get("licenseFile"):
            to_fetch.append(entry["licenseFile"])

    missing_locally = [p for p in to_fetch if not (dist_dir / p).exists()]
    if not missing_locally:
        print("dist/ already has every file the manifest references — nothing to re-download.")
        return

    print(f"Re-downloading {len(missing_locally)} already-published files from {base_url} ...")
    failed = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(download, base_url, p, dist_dir): p for p in missing_locally}
        for i, future in enumerate(as_completed(futures), 1):
            p = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"  FAILED {p}: {e}", file=sys.stderr)
                failed.append(p)
            if i % 200 == 0:
                print(f"  ...{i}/{len(missing_locally)}")

    print(f"Re-downloaded {len(missing_locally) - len(failed)}/{len(missing_locally)} files")
    if failed:
        print(f"FATAL: {len(failed)} files failed to re-download — dist/ would be incomplete, "
              f"aborting instead of deploying a broken snapshot.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
