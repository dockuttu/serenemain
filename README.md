# serenemain — serenemedspas.com (static)

Static snapshot of the former WordPress site, served from the VPS behind Traefik (same pattern as
serenebarboursville / serenehudson). Migrated Sep 22–23, 2026 ahead of LegitScript review.

## Redesign (Sep 23, 2026)
The WordPress look is gone: `gen_site.py` builds a new, hand-designed site from the snapshot's *content* (titles, meta, article bodies,
self-contained HTML tools) plus authored pages. Palette (v1, Sep 23 AM): deep teal / sage / sand; type: Cormorant Garamond + Jost. Superseded by v2 below.
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

## Design system v2 (Sep 23, 2026 — "best med spa site" pass)
Modeled on the top-grossing US med spa sites (SkinSpirit first; Ever/Body, Ject, Skin Laundry, LaserAway studied live):
serif display + geometric sans, one deep green, one soft accent, white space, pill buttons, uppercase letter-spaced labels.
- Type: **Poppins** (body, 300–600) · **Noto Serif Display** (h1/h2 uppercase, h3 normal case) · **Oooh Baby** (script accents, `.script`). All Google Fonts.
- Color tokens in `site_lib.CSS :root`: `--forest #10322F` (primary; a hair toward the logo teal), `--forest-700/-500`, `--lav #C4C7E6` + `--lav-100` (accent; promo bar, eyebrows, trust strip, offer panel), `--grey #F5F7FA` (alternate sections), ink `#121417`. Legacy `--teal-*`/`--sage`/`--sand` names alias to these so older templates keep working.
- Components: `.eyebrow` (lavender label), `.trust` strip, `.arch` (arch-shaped category photos), `.loctile` (photo location cards), `.provcard`, `.offer` (20% first-visit panel), `.rev` quote cards on `.tint-teal`, `.locpick` header location chooser, footer newsletter (`#zf-news` → Zoho web-to-lead, Last Name "Email signup", LEADCF1 "Website form: newsletter").
- Real photos live in `assets/img/` (copied from the location sites' `img/`) and are served at `/img/…`; the WordPress uploads still serve at `/wp-content/uploads/…`.
- Location memory: the header "Choose location" pill stores `serene_loc` (hudson | barboursville | telehealth) in localStorage; any `[data-loc-book]` / `[data-loc-tel]` link and `[data-loc-name]` text swaps to that office; `[data-loc-only="hudson"]` blocks show only for that office.
- Monthly specials: `pages_custom.SPECIALS_MONTH` / `SPECIALS` (no flyer image needed); the promo bar text is `site_lib.PROMO`.

## Plan: fold hudson. and barboursville. into serenemedspas.com (approved Sep 23)
Goal: one brand, one nav, one domain for SEO — `serenemedspas.com/hudson/…` and `/barboursville/…`, 301 from every subdomain URL.
1. **Phase 1 (done):** main site on the v2 design; header location chooser; location tiles link to the subdomains for now.
2. **Phase 2 — Barboursville (DONE Sep 23, 2026; ~190 pages):** the serenebarboursville build got a final pass, `v2_merge.py`, that prefixes every URL with `/barboursville`, rewrites the host, and swaps in this repo's v2 header/footer (imported from `site_lib.py` on the VPS at `/root/serenemain-src`). The main container bind-mounts `/root/barboursville` and serves it via `location ^~ /barboursville/ { alias … }` (see `bundle/nginx.conf`, `bundle/docker-compose.yml`). `barboursville.serenemedspas.com` is redirect-only (301, query string preserved). `/barboursville/sitemap.xml` submitted to Search Console and listed in robots.txt. Still to do (Robin's OK needed): Google Ads final URLs `/lp/*` → `/barboursville/lp/*`, GBP website link, Mangomint links.
3. **Phase 3 — Hudson (DONE Sep 23, 2026; ~190 pages incl. Obagi shop, labs, aftercare, city SEO pages):** same mechanism as Phase 2 — `v2_merge.py` in serenehudson (PREFIX `/hudson`), main container mounts `/root/hudson` at `/srv/hudson`, `location ^~ /hudson/ { alias … }`, `hudson.serenemedspas.com` redirect-only. `/hudson/sitemap.xml` in robots.txt + Search Console.
4. **Polish (DONE Sep 23, 2026):** `site_lib.LOCAL_MAP` maps main-site article slugs to office page slugs (`LOCAL_MISSING` lists office gaps). Once an office is chosen, `localize()` in SCRIPTS rewrites header/footer/sidebar/card links to `/<office>/<slug>/` (originals kept in `data-orig`; Telehealth or no choice restores them). Articles get a 'Local pricing' sidebar card linking both offices' pages. Office pages (`v2_merge.py` in each location repo) set the visitor's office to that page's office — page context wins over the remembered choice. Remaining: retire the two subdomain containers after ~12 months of redirects.
Rules: never change DNS or Google Ads final URLs without Robin's OK; keep the free-card pages untouched; every old URL must 301 (check with `check_links.py` + Search Console coverage after each phase).
5. **SEO pass 2 (DONE Sep 23, 2026):** `seo_meta.py` (per-page titles/descriptions/JSON-LD + default BreadcrumbList/WebPage, applied in `site_lib.shell()`), `post_overrides.py` (article title/description/price-Offer overrides, author → provider Person LD; articles get Article + BreadcrumbList + FAQPage when ≥2 Q&As), `optimize_images.py` (Mac, Pillow → `assets/webp/` variants + manifest, committed) and `imgopt.py` (VPS, stdlib: copies variants, rewrites `<img>` to srcset/sizes/lazy, preloads the hero). Duplicate-slug articles and retired URLs are 301'd via `_redirects.map` (written by `gen_site.py` into the site root, loaded by `map $uri $moved_to` in `bundle/nginx.conf`, hidden from the web). `guides.json` (slug → related main-site guides) feeds the office builds' "From our treatment guides" blocks.
   - nginx gotchas learned the hard way: the map keys are long URLs, so `map_hash_bucket_size 128;` is required (default 64 → container crash-loops with "could not build map_hash"); `absolute_redirect off;` keeps 301 Location headers relative (nginx listens on :80 behind Traefik, so absolute redirects would bounce through http://). Validate config changes against the REAL `_redirects.map` (`nginx -t`) before pushing.
