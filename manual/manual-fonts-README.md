# Adding manual fonts

This covers fonts that come from anywhere other than `google/fonts` (i.e. anything
not listed in `families.yaml`). Drop them under `manual/` and point `--sources` at
the right subfolder(s), matching what `.github/workflows/build-and-deploy.yml`
already does (`manual/general`, `manual/itf/ffl`, `manual/itf/ofl`, `manual/fontsource`,
etc. — the subfolder names are just organizational; the pipeline only cares about
the *contents* of each family folder, described below).

There are three formats the pipeline recognizes. Which one you use depends on
whether you're handing it raw font files, an already-built web-font drop, or a
Fontsource package.

---

## Format A — `family.yaml` folder (most common)

Save a file named exactly, "family.yaml" in every folder. Use this for anything you're handing the pipeline as `.ttf`/`.otf`/`.woff2`
files directly — a font you downloaded from a foundry, a variable font, a
personal/commissioned font, etc.

```
manual/general/
  your-font-name/
    family.yaml
    YourFont-Regular.ttf
    YourFont-Bold.ttf
    OFL.txt
```

**`family.yaml` fields:**

| Field      | Required? | Notes |
|------------|-----------|-------|
| `family`   | yes       | Display name, e.g. `My Custom Font` |
| `license`  | yes       | Must be one of: `OFL`, `OFL-1.1`, `Apache-2.0`, `APACHE2`, `MIT`, `UFL`, `UFL-1.0`, `CC0`, `FFL`. Anything else gets skipped with a warning. |
| `designer` | no        | Defaults to `Unknown` |
| `category` | no        | e.g. `sans-serif`, `serif`, `display`. Defaults to `unknown` |

```yaml
family: My Custom Font
license: OFL
designer: Jane Doe
category: sans-serif
```

**License file:** put the actual license text in the folder as `OFL.txt`,
`LICENSE.txt`, `UFL.txt`, or `LICENSE` — one of those exact filenames, sitting
directly in the family folder (not a subfolder). It gets copied into the
output alongside the fonts.

**Font files:** drop `.ttf`, `.otf`, and/or `.woff2` files straight in the
family folder, next to `family.yaml`. No particular naming convention is
required — style/weight are read from each font's own name table and OS/2
table, not from the filename.

- **`.ttf` / `.otf`** → the pipeline subsets these per Unicode range and
  builds `.woff2` output itself (via `pyftsubset`).
- **`.woff2`** → treated as already built. The pipeline copies it through
  as-is (still detecting its Unicode coverage for the manifest, just not
  re-encoding it).

You can mix both in the same folder — e.g. a variable `.ttf` that needs
subsetting alongside a hinted `.woff2` you want passed through untouched.
Each file is judged individually by its own extension.

---

## Format B — ITF/Fontshare-style drop (pre-built, no `family.yaml`)

This is for drops that already come packaged the way Indian Type Foundry /
Fontshare ships them, with their own CSS and folder layout. If your family
folder looks like this, skip `family.yaml` entirely — it's not read for this
format:

```
manual/itf/ofl/
  your-font-name/
    Fonts/
      WEB/
        css/
          your-font-name.css       ← must contain a "Font Family: ..." comment line
        fonts/
          YourFont-Regular.woff2
          YourFont-Bold.woff2
    License/
      OFL.txt                       ← or FFL.txt
```

The pipeline detects this shape by the presence of `Fonts/WEB/css/*.css`.
From that CSS file it reads:
- the family name, from a `Font Family: ...` comment line in the header,
- each font's weight/style/filename, from the `@font-face` blocks.

License comes from `License/OFL.txt` or `License/FFL.txt` (whichever is
present) — this is a different location than Format A's license file, which
lives directly in the family folder.

All fonts in this format are treated as pre-built and copied through as-is,
same as a `.woff2` file would be in Format A.

---

## Format C — Fontsource package (pre-built, no `family.yaml`)

This is for a family exactly as Fontsource ships it in its npm package — drop
the package's contents straight in, unzipped/untarred, no changes:

| You have...                                              | Use |
|-----------------------------------------------------------|-----|
| Raw `.ttf`/`.otf` you want subsetted into `.woff2`          | Format A, with the `.ttf`/`.otf` files |
| Already-built `.woff2` from somewhere ad hoc                | Format A, with the `.woff2` files — write a `family.yaml` |
| A mix of both, for the same family                          | Format A — drop both kinds in one folder |
| An actual ITF/Fontshare "Fonts/WEB/..." zip, unzipped as-is  | Format B — no `family.yaml` needed |

---

## Troubleshooting

- **`SKIP <folder>: no METADATA.pb and no family.yaml`** — the pipeline didn't
  find `METADATA.pb` (Google shape) or `family.yaml` (Format A), and the
  folder doesn't have the `Fonts/WEB/css` shape either (Format B). Add a
  `family.yaml`.
- **`SKIP <family>: produced zero files`** — the family was recognized but no
  usable font files were found. For Format A, double check your font files
  end in `.ttf`, `.otf`, or `.woff2` and sit directly in the family folder
  (not a subfolder).
- **`SKIP <family>: license '...' not in allowlist`** — check the `license:`
  value in `family.yaml` against the allowed list above (case-sensitive).
- **weight mismatch warning** — informational only; it means the font's
  internal weight number and its style name (e.g. "Bold") disagreed by more
  than 100, and the pipeline used the name-derived value. Worth a quick look
  at the font file if it seems wrong.
