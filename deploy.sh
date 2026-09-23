#!/usr/bin/env bash
# deploy.sh — git-based deploy for serenemedspas.com (main site, static snapshot of the former WordPress site)
#
# Runs ON THE VPS from the cloned repo (default: /root/serenemain-src), called by /root/autodeploy.sh
# whenever GitHub main is ahead of what is live. Pulls, builds into bundle/site, promotes atomically
# to /root/serenemain/site and (re)starts the nginx container behind Traefik.
set -euo pipefail

SRC="${SRC:-/root/serenemain-src}"
LIVE="${LIVE:-/root/serenemain}"
BRANCH="${BRANCH:-main}"

cd "$SRC"
echo "==> Pulling latest ($BRANCH)"
git fetch --all --quiet
git reset --hard "origin/$BRANCH"
echo "    now at: $(git rev-parse --short HEAD) — $(git log -1 --pretty=%s)"

echo "==> Building"
./build.sh

mkdir -p "$LIVE"
echo "==> Promoting to live ($LIVE/site) atomically"
rm -rf "$LIVE/site.new"
cp -a bundle/site "$LIVE/site.new"
rm -rf "$LIVE/site.old"
[ -d "$LIVE/site" ] && mv "$LIVE/site" "$LIVE/site.old"
mv "$LIVE/site.new" "$LIVE/site"

cp -f bundle/docker-compose.yml "$LIVE/docker-compose.yml"
cp -f bundle/nginx.conf "$LIVE/nginx.conf"

echo "==> Restarting container"
cd "$LIVE"
docker compose up -d --force-recreate --remove-orphans
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'NAMES|serenemain' || true
echo "==> Deploy complete. Rollback:  rm -rf $LIVE/site && mv $LIVE/site.old $LIVE/site && cd $LIVE && docker compose up -d --force-recreate"
