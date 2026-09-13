# Manual (non-Google) font sources

Fonts from anywhere other than `google/fonts` — Velvetyne, League of
Moveable Type, a foundry's own GitHub repo, etc. — go here, one folder per
family.

Unlike `google/fonts`, these sources don't ship a `METADATA.pb`, so the
pipeline can't derive the license (or the family display name) from the
file itself — you supply that in a small sidecar.

## Contract

```
manual/
  your-font-slug/
    YourFont-Regular.ttf        # any number of .ttf/.otf files
    YourFont-Bold.ttf
    family.yaml                 # required
    LICENSE.txt / OFL.txt       # strongly recommended — copy the upstream license file
```

`family.yaml`:

```yaml
family: "Your Font"             # required — display name
license: "OFL-1.1"              # required — must be one of the allowed licenses below
designer: "Foundry Name"        # optional, defaults to "Unknown"
category: "sans-serif"          # optional, defaults to "unknown"
source_url: "https://github.com/foundry/your-font"   # optional but recommended, for provenance
```

Allowed `license` values (edit `ALLOWED_LICENSES` in `scripts/pipeline.py`
if you need to add one — the point of the allowlist is that you're making a
deliberate decision each time, not that this exact list is final):

```
OFL, OFL-1.1, Apache-2.0, APACHE2, MIT, UFL, UFL-1.0, CC0
```

If `family.yaml` is missing or the license isn't on the allowlist, the
pipeline **skips that family with a warning** rather than guessing — check
the Action log if a font you added doesn't show up in the manifest.

## What happens automatically

Everything else — weight, style (normal/italic), and which unicode
subsets (latin, cyrillic, vietnamese, etc.) the font actually covers — is
detected directly from the font file, using the same detection logic used
for Google sources. You don't need to fill any of that in.
