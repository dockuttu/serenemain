#!/usr/bin/env bash
# Standalone build (NOT used by serenemain): renders into ../../bundle/paintsville/site next to this folder's parent.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 gen_site.py "${1:-../bundle/paintsville/site}"
