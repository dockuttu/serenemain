# serenemain — serenemedspas.com (static)

Static snapshot of the former WordPress site, served from the VPS behind Traefik (same pattern as
serenebarboursville / serenehudson). Migrated Sep 22–23, 2026 ahead of LegitScript review.

## Redesign (Sep 23, 2026)
The WordPress look is gone: `gen_site.py` builds a new, hand-designed site from the snapshot's *content* (titles, meta, article bodies,
self-contained HTML tools) plus authored pages. Palette: deep teal / sage / sand (matches the Serene logo); type: Cormorant Garamond + Jost.
- `site_lib.py` — brand constants, CSS (`/main.css`), header/nav/footer shell, consult form, booking band, tracking (Google Ads tag + Meta pixel).
- `extract.py` — pulls meta + clean semantic HTML out of the Elementor pages (posts -> `.prose`; pasted HTML tools -> embedded as-is).
- `pages_custom.py` — home, locations, providers, about, reviews, membership, financing, specials, telehealth (with LegitScript disclosures), thank-you.
- `gen_site.py` — inventory + categories + renderers: 116 treatment articles (duplicates canonicalized), `/service/` directory, `/blogs/` index, redirects.
- Retired WordPress paths and legacy broken links are 301'd in `bundle/nginx.conf`. `/wrinkle-treatments/` -> Hudson site /botox/.
Editing copy: authored pages in `pages_custom.py`; article bodies still come from `mirror/<slug>/index.html` (Elementor markup is simplified at build).

- `mirror/` — raw snapshot of the live WordPress site (made with `mirror.py` on the Mac). Source of truth for page content.
- `clean_mirror.py` — strips WordPress-only plumbing (WooCommerce, Jetpack, Ultimate Member, emoji, discovery links), re-absolutizes canonical/og/JSON-LD URLs, drops cart/checkout/account/shop pages.
- `overlays.py` — telehealth disclosures (`telehealth-disclosures.html`), branded 404, sitemap.xml, robots.txt.
- `build.sh` → `bundle/site/` (not committed; the VPS builds it). `deploy.sh` runs on the VPS via /root/autodeploy.sh.
- `bundle/nginx.conf` — www→apex, retired WP paths → 301/410, `/shop/` → Barboursville Obagi shop, `/blog/` → blog.serenemedspas.com.

Editing a page: edit the file under `mirror/<slug>/index.html`, commit, push — live within ~2 minutes.
Rollback of the whole migration: point DNS for serenemedspas.com back at the Hostinger WordPress host.
