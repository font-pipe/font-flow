#!/usr/bin/env python3
"""
Guard against deploying a manifest that's drastically smaller than what's
currently live. This is exactly the shape a cache-restore miss produces:
dist/ never restores, pipeline.py's additive merge starts from an empty
manifest, and the run "succeeds" with only whatever it reprocessed this
time. Comparing against the local starting count can't catch that (it's
also zero) — comparing against the live site can.

Usage:
    python3 scripts/sanity_check_manifest.py <production_manifest_url> <path_to_new_manifest.json>
"""
import json
import sys
import urllib.error
import urllib.request

MIN_RATIO = 0.9  # new manifest must have at least 90% of the live family count


def main():
    if len(sys.argv) != 3:
        print("Usage: sanity_check_manifest.py <production_manifest_url> <new_manifest_path>", file=sys.stderr)
        sys.exit(2)

    prod_url, new_path = sys.argv[1], sys.argv[2]

    # Plain urllib requests default to a "Python-urllib/x.y" User-Agent,
    # which Cloudflare's Bot Fight Mode blocks outright (403) even though
    # the request itself is completely legitimate — it's just fetching a
    # public JSON file. A normal browser-shaped User-Agent clears that.
    request = urllib.request.Request(
        prod_url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; font-flow-sanity-check/1.0)"},
    )
    try:
        with urllib.request.urlopen(request) as resp:
            prod_count = len(json.loads(resp.read()).get("fonts", []))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("No manifest currently live (404) — nothing to compare against, allowing deploy.")
            return
        raise

    new_count = len(json.loads(open(new_path).read()).get("fonts", []))
    print(f"Live manifest: {prod_count} families. New manifest: {new_count} families.")

    if new_count < prod_count * MIN_RATIO:
        print(
            f"ABORT: new manifest ({new_count} families) is far smaller than what's "
            f"currently live ({prod_count} families). Refusing to deploy — this almost "
            f"always means dist/ failed to restore from cache rather than families being "
            f"legitimately removed.",
            file=sys.stderr,
        )
        sys.exit(1)

    print("OK — manifest size looks sane, proceeding.")


if __name__ == "__main__":
    main()
