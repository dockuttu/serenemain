#!/usr/bin/env bash
# deploy.sh — STANDALONE ONLY (not used when this folder lives inside serenemain; see ../DEPLOY-SNIPPETS.md).
# Modeled on the Hudson deploy pattern:  /root/serenepaintsville/{site,docker-compose.yml,nginx.conf}
#
#   ssh root@vps 'bash -s' < deploy.sh        # or run it from a clone on the VPS
#
# Prereqs on the VPS: git, python3 (+ Pillow for image variants: pip3 install pillow), docker compose,
# the shared traefik network "root_default", and the repo cloned at $REPO.
set -euo pipefail
REPO="${REPO:-/root/src/serenepaintsville}"          # git checkout of this repo
LIVE="${LIVE:-/root/serenepaintsville}"              # docker-compose lives here; site is served from $LIVE/site
BRANCH="${BRANCH:-main}"

echo "==> pull"
git -C "$REPO" fetch --quiet origin "$BRANCH"
git -C "$REPO" reset --hard --quiet "origin/$BRANCH"

echo "==> build"
(cd "$REPO" && python3 gen_site.py bundle/site)

echo "==> promote"
mkdir -p "$LIVE"
cp "$REPO/_standalone/docker-compose.yml" "$LIVE/docker-compose.yml"
cp "$REPO/nginx.conf" "$LIVE/nginx.conf"
STAMP="$(date +%Y%m%d-%H%M%S)"
rsync -a --delete "$REPO/bundle/site/" "$LIVE/site-$STAMP/"
if [ -L "$LIVE/site" ] || [ ! -e "$LIVE/site" ]; then
  ln -sfn "site-$STAMP" "$LIVE/site.tmp" && mv -Tf "$LIVE/site.tmp" "$LIVE/site"     # atomic symlink swap
else
  mv "$LIVE/site" "$LIVE/site-prev-$STAMP" && ln -sfn "site-$STAMP" "$LIVE/site"      # first run: replace a real dir
fi
# keep the last 3 releases
ls -1dt "$LIVE"/site-* 2>/dev/null | tail -n +4 | xargs -r rm -rf

echo "==> docker"
(cd "$LIVE" && docker compose up -d --remove-orphans)
echo "==> done: https://serenemedspaky.com"
