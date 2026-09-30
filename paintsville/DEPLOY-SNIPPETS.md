# Wiring `paintsville/` into the serenemain repo

This folder is copied to `serenemain/paintsville/`. It builds serenemedspaky.com into
`serenemain/bundle/paintsville/site/` and is served by its own nginx container behind the shared traefik.
Add the four snippets below to serenemain; nothing else changes.

## (a) `serenemain/build.sh` — append after the main-site build

```bash
echo "==> Paintsville (serenemedspaky.com)"
python3 paintsville/gen_site.py bundle/paintsville/site || echo "!!! paintsville build failed (continuing)" >&2
```

## (b) `serenemain/bundle/docker-compose.yml` — add a service (same `networks:` block already exists)

```yaml
  paintsville:
    image: nginx:alpine
    container_name: paintsville-site
    restart: always
    volumes:
      - ./paintsville/site:/usr/share/nginx/html:ro
      - ./paintsville/nginx.conf:/etc/nginx/conf.d/default.conf:ro
    networks:
      - root_default
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.paintsville.rule=Host(`serenemedspaky.com`) || Host(`www.serenemedspaky.com`)"
      - "traefik.http.routers.paintsville.entrypoints=web,websecure"
      - "traefik.http.routers.paintsville.tls=true"
      - "traefik.http.routers.paintsville.tls.certresolver=mytlschallenge"
      - "traefik.http.routers.paintsville.tls.domains[0].main=serenemedspaky.com"
      - "traefik.http.routers.paintsville.tls.domains[0].sans=www.serenemedspaky.com"
      - "traefik.http.services.paintsville.loadbalancer.server.port=80"
```

## (c) `serenemain/deploy.sh` — after the main-site promote (uses the same `.new`/`.old` swap; `$LIVE` = live bundle dir)

```bash
if [ -d bundle/paintsville/site ]; then
  echo "==> promote paintsville"
  mkdir -p "$LIVE/paintsville"
  rm -rf "$LIVE/paintsville/site.new" "$LIVE/paintsville/site.old"
  cp -a bundle/paintsville/site "$LIVE/paintsville/site.new"
  cp -f paintsville/nginx.conf "$LIVE/paintsville/nginx.conf"
  [ -d "$LIVE/paintsville/site" ] && mv "$LIVE/paintsville/site" "$LIVE/paintsville/site.old"
  mv "$LIVE/paintsville/site.new" "$LIVE/paintsville/site"
  rm -rf "$LIVE/paintsville/site.old"
fi
```

(`docker compose up -d` at the end of deploy.sh picks up the new `paintsville` service; nginx serves the
swapped directory without a restart. DNS: point `serenemedspaky.com` and `www` at the VPS; traefik issues the cert.)

## (d) `serenemain/.gitignore` — add

```
bundle/paintsville/site/
```
