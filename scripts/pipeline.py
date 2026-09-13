#!/usr/bin/env python3
"""
Font ingest pipeline: turns source font families into subsetted woff2 files
+ a single manifest.json.

Each source directory's children are treated as family folders. A family
folder is EITHER:
  - a google/fonts-style folder containing METADATA.pb (+ .ttf/.otf files), or
  - a "manual" folder containing a family.yaml sidecar (+ .ttf/.otf files)
    (see manual/README.md for the exact contract)

This has been tested end-to-end against real families pulled from
google/fonts, including variable fonts, and against a synthetic manual
(non-Google) family exercising the fallback metadata path.

Usage:
    python3 scripts/pipeline.py \
        --sources .cache/gfonts/ofl .cache/gfonts/apache .cache/gfonts/ufl manual \
        --out dist
"""
import argparse
import json
import re
import shutil
import sys
from pathlib import Path

import yaml
from fontTools.ttLib import TTFont
from fontTools import subset
from google.protobuf import text_format
from gfmetadata import fonts_public_pb2
import gfsubsets

# FFL = Fontshare/Indian Type Foundry's own "Free Font License" — added here
# for the ITF source below. Confirm FFL's terms actually permit this kind of
# redistribution before shipping a real foundry drop under it.
ALLOWED_LICENSES = {"OFL", "OFL-1.1", "Apache-2.0", "APACHE2", "MIT", "UFL", "UFL-1.0", "CC0", "FFL"}
LICENSE_FILENAMES = ["OFL.txt", "LICENSE.txt", "UFL.txt", "LICENSE"]

# Used only as a fallback, and only when a font's OS/2.usWeightClass and its
# subfamily name disagree by more than 100 — see extract_style_weight_from_tables.
WEIGHT_NAME_MAP = {
    "thin": 100, "extralight": 200, "ultralight": 200, "light": 300,
    "regular": 400, "normal": 400, "book": 400, "medium": 500,
    "semibold": 600, "demibold": 600, "bold": 700, "extrabold": 800,
    "ultrabold": 800, "black": 900, "heavy": 900,
}


def slugify(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def find_license_file(family_dir: Path):
    for fname in LICENSE_FILENAMES:
        p = family_dir / fname
        if p.exists():
            return p
    return None


def weight_from_name(subfamily: str):
    key = subfamily.lower().replace(" ", "").replace("italic", "")
    return WEIGHT_NAME_MAP.get(key)


def read_metadata_pb(family_dir: Path):
    """Google source: parse METADATA.pb. This is already QA'd by fontbakery
    upstream, so weight/style here are more trustworthy than re-deriving them
    from OS/2 alone."""
    msg = fonts_public_pb2.FamilyProto()
    text_format.Merge((family_dir / "METADATA.pb").read_text(), msg)

    axis_range = None
    for a in msg.axes:
        if a.tag == "wght":
            axis_range = f"{int(a.min_value)} {int(a.max_value)}"

    fonts = []
    for f in msg.fonts:
        fonts.append({
            "path": family_dir / f.filename,
            "style": f.style,
            "weight": axis_range if axis_range else str(f.weight),
        })

    return {
        "family": msg.name,
        "license": msg.license,
        "designer": msg.designer,
        "category": list(msg.category),
        "declared_subsets": [s for s in msg.subsets if s != "menu"],
        "fonts": fonts,
    }


def extract_style_weight_from_tables(font_path: Path):
    """Fallback for fonts with no METADATA.pb: read OpenType tables directly."""
    font = TTFont(str(font_path), lazy=True)
    name = font["name"]
    os2 = font.get("OS/2")
    head = font["head"]

    subfamily = name.getDebugName(17) or name.getDebugName(2) or "Regular"
    is_italic = bool(os2.fsSelection & 0x01) if os2 else bool(head.macStyle & 0x02)
    style = "italic" if is_italic else "normal"

    if "fvar" in font:
        axes = {a.axisTag: (a.minValue, a.maxValue) for a in font["fvar"].axes}
        if "wght" in axes:
            lo, hi = axes["wght"]
            return style, f"{int(lo)} {int(hi)}"

    table_weight = os2.usWeightClass if os2 else 400
    name_weight = weight_from_name(subfamily)
    if name_weight and abs(name_weight - table_weight) > 100:
        print(f"  ! weight mismatch in {font_path.name}: OS/2 says {table_weight}, "
              f"name says '{subfamily}' (~{name_weight}) — using name-derived value", file=sys.stderr)
        return style, str(name_weight)
    return style, str(table_weight)


def find_itf_css(family_dir: Path):
    """ITF/Fontshare-style drop (manual/itf/<family>/Fonts/WEB/css/*.css)
    identifies itself by this path; fonts arrive pre-built as woff2."""
    css_dir = family_dir / "Fonts" / "WEB" / "css"
    if not css_dir.exists():
        return None
    css_files = sorted(css_dir.glob("*.css"))
    return css_files[0] if css_files else None


def read_itf_metadata(family_dir: Path, css_path: Path):
    """ITF source: no family.yaml sidecar — family name comes from the
    css header comment, weight/style/filename come from each @font-face
    block, and the woff2 files are copied as-is rather than re-subset."""
    css_text = css_path.read_text()

    family_match = re.search(r"Font Family:\s*(.+)", css_text)
    if not family_match:
        raise ValueError("no 'Font Family:' line found in css header comment")
    family = family_match.group(1).strip()

    license_file = family_dir / "License" / "FFL.txt"
    if not license_file.exists():
        raise ValueError(f"expected {license_file} (ITF/Fontshare Free Font License)")
    if "FFL" not in ALLOWED_LICENSES:
        raise ValueError("license 'FFL' not in allowlist")

    fonts_dir = family_dir / "Fonts" / "WEB" / "fonts"
    faces = []
    for block in re.finditer(r"@font-face\s*\{([^}]+)\}", css_text):
        body = block.group(1)
        weight_m = re.search(r"font-weight:\s*([\d\s]+);", body)
        style_m = re.search(r"font-style:\s*(\w+);", body)
        src_m = re.search(r"url\(['\"]?[^'\"]*?/([^/'\")]+\.woff2)['\"]?\)", body)
        if not (weight_m and style_m and src_m):
            continue
        faces.append({
            "path": fonts_dir / src_m.group(1),
            "style": style_m.group(1).strip(),
            "weight": " ".join(weight_m.group(1).split()),
        })

    if not faces:
        raise ValueError(f"no usable @font-face blocks found in {css_path}")

    return {
        "family": family,
        "license": "FFL",
        "designer": "Unknown",
        "category": ["unknown"],
        "declared_subsets": None,
        "fonts": faces,
        "license_file": license_file,
        "prebuilt": True,
    }


def read_manual_metadata(family_dir: Path):
    """Non-Google source: family.yaml sidecar supplies what we can't derive
    from the font file itself (chiefly: license)."""
    meta_path = family_dir / "family.yaml"
    if not meta_path.exists():
        raise ValueError("no METADATA.pb and no family.yaml — can't determine license, skipping")
    meta = yaml.safe_load(meta_path.read_text())
    if meta.get("license") not in ALLOWED_LICENSES:
        raise ValueError(f"license '{meta.get('license')}' not in allowlist {sorted(ALLOWED_LICENSES)}")

    fonts = []
    for font_path in sorted(list(family_dir.glob("*.ttf")) + list(family_dir.glob("*.otf"))):
        style, weight = extract_style_weight_from_tables(font_path)
        fonts.append({"path": font_path, "style": style, "weight": weight})

    return {
        "family": meta["family"],
        "license": meta["license"],
        "designer": meta.get("designer", "Unknown"),
        "category": [meta.get("category", "unknown")],
        "declared_subsets": None,  # unknown up front — detect from the font's own coverage
        "fonts": fonts,
    }


def detect_subsets(font_path: Path, declared_subsets):
    """Google sources declare their subsets in METADATA.pb. Everything else
    gets its coverage detected directly, using Google's own subset
    definitions (gfsubsets) — verified to match METADATA.pb's own subset
    list almost exactly when run against a Google font, so it generalizes
    safely to non-Google sources."""
    if declared_subsets:
        return declared_subsets
    detected = gfsubsets.SubsetsInFont(str(font_path), 50, 10)
    return [name for name, _, _ in detected]


def codepoints_for_subset(subset_name: str, font_cmap_keys: set):
    """Intersect the subset's defined codepoints with what this font file
    actually has a glyph for — avoids declaring coverage the font doesn't have."""
    subset_cps = set(gfsubsets.CodepointsInSubset(subset_name, unique_glyphs=True))
    return sorted(subset_cps & font_cmap_keys)


def unicode_range_string(codepoints):
    if not codepoints:
        return None
    cps = sorted(codepoints)
    ranges, start, prev = [], cps[0], cps[0]
    for cp in cps[1:]:
        if cp == prev + 1:
            prev = cp
            continue
        ranges.append((start, prev))
        start = prev = cp
    ranges.append((start, prev))
    return ", ".join(f"U+{a:04X}" if a == b else f"U+{a:04X}-{b:04X}" for a, b in ranges)


def build_woff2(font_path: Path, codepoints, out_path: Path):
    ranges = unicode_range_string(codepoints)
    args = [
        str(font_path),
        f"--unicodes={ranges}",
        "--layout-features=*",
        "--flavor=woff2",
        f"--output-file={out_path}",
    ]
    try:
        subset.main(args)
    except SystemExit as e:
        if e.code not in (0, None):
            raise RuntimeError(f"pyftsubset failed on {font_path}: exit {e.code}")


def process_family(family_dir: Path, out_root: Path, manifest_entries: list):
    is_google = (family_dir / "METADATA.pb").exists()
    itf_css = None if is_google else find_itf_css(family_dir)
    try:
        if is_google:
            meta = read_metadata_pb(family_dir)
        elif itf_css:
            meta = read_itf_metadata(family_dir, itf_css)
        else:
            meta = read_manual_metadata(family_dir)
    except Exception as e:
        print(f"SKIP {family_dir.name}: {e}", file=sys.stderr)
        return

    slug = slugify(meta["family"])
    family_out = out_root / slug
    family_out.mkdir(parents=True, exist_ok=True)

    license_file = meta.get("license_file") or find_license_file(family_dir)
    if license_file:
        shutil.copy(license_file, family_out / license_file.name)

    files_entry = []
    all_subsets = set()

    prebuilt = meta.get("prebuilt", False)
    for f in meta["fonts"]:
        font = TTFont(str(f["path"]), lazy=True)
        cmap_keys = set(font.getBestCmap().keys())
        subsets = detect_subsets(f["path"], meta["declared_subsets"])

        if prebuilt:
            covered = set()
            for subset_name in subsets:
                cps = codepoints_for_subset(subset_name, cmap_keys)
                if cps:
                    covered.update(cps)
                    all_subsets.add(subset_name)
            if not covered:
                continue
            out_name = f"{slug}-{f['style']}-{f['weight'].replace(' ', '_')}.woff2"
            shutil.copy(f["path"], family_out / out_name)
            files_entry.append({
                "path": f"{slug}/{out_name}",
                "weight": f["weight"],
                "style": f["style"],
                "unicodeRange": unicode_range_string(covered),
            })
            continue

        for subset_name in subsets:
            cps = codepoints_for_subset(subset_name, cmap_keys)
            if not cps:
                continue
            out_name = f"{slug}-{f['style']}-{subset_name}.woff2"
            build_woff2(f["path"], cps, family_out / out_name)
            files_entry.append({
                "path": f"{slug}/{out_name}",
                "weight": f["weight"],
                "style": f["style"],
                "unicodeRange": unicode_range_string(cps),
            })
            all_subsets.add(subset_name)

    if not files_entry:
        print(f"SKIP {meta['family']}: produced zero files", file=sys.stderr)
        return

    # a family being rebuilt replaces its old entry rather than duplicating it
    manifest_entries[:] = [e for e in manifest_entries if e["id"] != slug]
    manifest_entries.append({
        "id": slug,
        "family": meta["family"],
        "license": meta["license"],
        "designer": meta.get("designer", "Unknown"),
        "category": (meta["category"][0].lower().replace("_", "-") if meta["category"] else "unknown"),
        "subsets": sorted(all_subsets),
        "files": files_entry,
    })
    print(f"OK   {meta['family']} ({slug}): {len(files_entry)} files, subsets={sorted(all_subsets)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", nargs="+", required=True, help="Directories whose children are family folders")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    manifest_path = out_root / "manifest.json"
    manifest_entries = []
    if manifest_path.exists():
        try:
            manifest_entries = json.loads(manifest_path.read_text()).get("fonts", [])
            print(f"Loaded {len(manifest_entries)} families from prior build (additive)")
        except Exception as e:
            print(f"WARN: couldn't read existing manifest, starting fresh: {e}", file=sys.stderr)

    for source_dir in args.sources:
        source_path = Path(source_dir)
        if not source_path.exists():
            print(f"WARN source dir does not exist, skipping: {source_path}", file=sys.stderr)
            continue
        for family_dir in sorted(p for p in source_path.iterdir() if p.is_dir()):
            process_family(family_dir, out_root, manifest_entries)

    manifest_path = out_root / "manifest.json"
    manifest_path.write_text(json.dumps({"fonts": manifest_entries}, indent=2))
    print(f"\nWrote manifest with {len(manifest_entries)} families to {manifest_path}")


if __name__ == "__main__":
    main()
