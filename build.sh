#!/usr/bin/env bash
# build.sh — turn the WordPress snapshot in mirror/ into the static site in bundle/site/ (stdlib Python; idempotent)
set -euo pipefail
cd "$(dirname "$0")"
echo "==> Generate site from snapshot + templates"
python3 gen_site.py mirror bundle/site
echo "==> Images: WebP variants (generated where Pillow exists; otherwise the committed assets/webp/ set is used)"
python3 optimize_images.py bundle/site || echo "!!! optimize_images failed (continuing with committed variants)" >&2
python3 imgopt.py bundle/site
echo "==> Overlays (telehealth disclosures, 404, sitemap, robots)"
python3 overlays.py bundle/site
echo "==> Link check"
python3 check_links.py bundle/site | tail -8 || echo "!!! WARNING: some page links are missing (see above)" >&2
if [ ! -s bundle/site/index.html ] || [ "$(wc -c < bundle/site/index.html)" -lt 5000 ]; then
  echo "!!! sanity check FAILED (homepage missing/too small)" >&2; exit 1; fi
echo "==> Build complete: $(find bundle/site -type f | wc -l) files in bundle/site/"
