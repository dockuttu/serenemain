# serenemain — serenemedspas.com (static)

Static snapshot of the former WordPress site, served from the VPS behind Traefik (same pattern as
serenebarboursville / serenehudson). Migrated Sep 22–23, 2026 ahead of LegitScript review.

- `mirror/` — raw snapshot of the live WordPress site (made with `mirror.py` on the Mac). Source of truth for page content.
- `clean_mirror.py` — strips WordPress-only plumbing (WooCommerce, Jetpack, Ultimate Member, emoji, discovery links), re-absolutizes canonical/og/JSON-LD URLs, drops cart/checkout/account/shop pages.
- `overlays.py` — telehealth disclosures (`telehealth-disclosures.html`), branded 404, sitemap.xml, robots.txt.
- `build.sh` → `bundle/site/` (not committed; the VPS builds it). `deploy.sh` runs on the VPS via /root/autodeploy.sh.
- `bundle/nginx.conf` — www→apex, retired WP paths → 301/410, `/shop/` → Barboursville Obagi shop, `/blog/` → blog.serenemedspas.com.

Editing a page: edit the file under `mirror/<slug>/index.html`, commit, push — live within ~2 minutes.
Rollback of the whole migration: point DNS for serenemedspas.com back at the Hostinger WordPress host.
