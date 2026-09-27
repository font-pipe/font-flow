#!/usr/bin/env python3
"""
Shared helper for talking to the manifest.json that's already live in
production. This is the single source of truth for "what's already been
built and shipped" — used instead of a GitHub Actions cache, which has no
reliable persistence (its save key here was accidentally scoped to each
run, and even fixed, caches still get evicted after 7 days idle or once
the repo's cache storage passes 10GB).

Imported by pipeline.py, fetch_google_families.py and
fetch_fontsource_families.py so all three agree on the same "already
published" set and the same source-id format.
"""
import json
import urllib.error
import urllib.request

# Replace with your actual Pages/R2 URL or custom domain — this same value
# is also hardcoded in sanity_check_manifest.py and build-and-deploy.yml;
# keep all three in sync if it ever changes.
DEFAULT_MANIFEST_URL = "https://font-flow.pages.dev/manifest.json"


def load_production_manifest(url: str = DEFAULT_MANIFEST_URL):
    """Fetch the live manifest.json. Returns its 'fonts' list, or [] if
    nothing has ever been deployed yet (a fresh repo's first-ever run)."""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; font-flow-pipeline/1.0)"},
    )
    try:
        with urllib.request.urlopen(request) as resp:
            return json.loads(resp.read()).get("fonts", [])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No manifest currently live (404) — starting from an empty baseline.")
            return []
        raise


def published_sources(manifest_entries):
    """Set of source ids (e.g. 'ofl/actor', 'manual/fontsource/inter')
    already represented in a manifest — i.e. already fetched and built at
    least once, so a normal run should skip redoing them."""
    return {e["source"] for e in manifest_entries if e.get("source")}
