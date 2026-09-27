#!/usr/bin/env python3
"""
Delete manual/ family folders whose slug now appears in the manifest we
just built and deployed. manual/ is a staging area, not permanent
storage — once a family's files are live on Cloudflare, there's no
reason to keep a copy in git too.

This only touches folders under the manual/ directories you pass in — it
never looks at .cache/gfonts (nothing there is ever git-tracked) or
manual/fontsource (fetch_fontsource_families.py re-downloads that fresh
every run, so it's already effectively transient).

Usage:
    python3 scripts/prune_published_manual_fonts.py dist/manifest.json manual/general manual/itf/ffl manual/itf/ofl
"""
import json
import shutil
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 3:
        print("Usage: prune_published_manual_fonts.py <manifest_path> <manual_dir> [<manual_dir> ...]", file=sys.stderr)
        sys.exit(2)

    manifest_path = Path(sys.argv[1])
    manual_dirs = [Path(p) for p in sys.argv[2:]]

    entries = json.loads(manifest_path.read_text()).get("fonts", [])
    published = {e["source"] for e in entries if e.get("source")}

    removed = []
    for manual_dir in manual_dirs:
        if not manual_dir.exists():
            continue
        for family_dir in sorted(p for p in manual_dir.iterdir() if p.is_dir()):
            source_id = family_dir.as_posix()
            if source_id in published:
                shutil.rmtree(family_dir)
                removed.append(source_id)

    if removed:
        print(f"Pruned {len(removed)} published manual families:")
        for r in removed:
            print(f"  - {r}")
    else:
        print("No published manual families to prune.")


if __name__ == "__main__":
    main()
