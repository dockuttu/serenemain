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

# bash keeps reading the deploy.sh it opened even after `git reset` swaps the file, so a changed deploy.sh
# would otherwise only take effect one deploy late. Re-exec the freshly pulled copy exactly once.
if [ -z "${DEPLOY_REEXEC:-}" ]; then
  echo "==> Re-running the freshly pulled deploy.sh"
  DEPLOY_REEXEC=1 exec bash "$0" "$@"
fi

echo "==> Building"
bash ./build.sh

mkdir -p "$LIVE"
echo "==> Promoting to live ($LIVE/site) atomically"
rm -rf "$LIVE/site.new"
cp -a bundle/site "$LIVE/site.new"
rm -rf "$LIVE/site.old"
[ -d "$LIVE/site" ] && mv "$LIVE/site" "$LIVE/site.old"
mv "$LIVE/site.new" "$LIVE/site"

echo "==> Paintsville (serenemedspaky.com): promote"
mkdir -p "$LIVE/paintsville"
# A failed first start leaves docker-auto-created *directories* at the bind-mount paths; clear the conf one.
if [ -d "$LIVE/paintsville/nginx.conf" ]; then rm -rf "$LIVE/paintsville/nginx.conf"; fi
cp -f paintsville/nginx.conf "$LIVE/paintsville/nginx.conf"
if [ -s bundle/paintsville/site/index.html ]; then
  rm -rf "$LIVE/paintsville/site.new" "$LIVE/paintsville/site.old"
  cp -a bundle/paintsville/site "$LIVE/paintsville/site.new"
  if [ -d "$LIVE/paintsville/site" ]; then mv "$LIVE/paintsville/site" "$LIVE/paintsville/site.old"; fi
  mv "$LIVE/paintsville/site.new" "$LIVE/paintsville/site"
  rm -rf "$LIVE/paintsville/site.old"
else
  echo "!!! paintsville build output missing — keeping whatever is live" >&2
  mkdir -p "$LIVE/paintsville/site"
fi

cp -f bundle/docker-compose.yml "$LIVE/docker-compose.yml"
cp -f bundle/nginx.conf "$LIVE/nginx.conf"

echo "==> Restarting container"
cd "$LIVE"
docker compose up -d --force-recreate --remove-orphans
docker ps --format 'table {{.Names}}\t{{.Status}}' | grep -E 'NAMES|serenemain|paintsville' || true
echo "==> Rebuilding the Hudson and Barboursville sites so /hudson/ and /barboursville/ pick up shared code + specials from this repo"
for sub in /root/hudson-src /root/barboursville-src; do
  if [ -f "$sub/deploy.sh" ]; then
    ( cd "$sub" && bash ./deploy.sh ) || echo "!!! $sub rebuild failed; its last good site stays live" >&2
  fi
done
echo "==> Deploy complete. Rollback:  rm -rf $LIVE/site && mv $LIVE/site.old $LIVE/site && cd $LIVE && docker compose up -d --force-recreate"
