# Serene Med Spa Paintsville, KY — serenemedspaky.com

Static-site generator for the Paintsville office site, packaged as the **`paintsville/` subfolder of the
serenemain repo** (same design system as serenemedspas.com, adapted for a single location). Python 3 stdlib only
at build time; output is plain HTML/CSS served by its own nginx container behind the shared traefik.

```
paintsville/
  gen_site.py        python3 paintsville/gen_site.py [out_dir]  — runs from any cwd; default out_dir is
                     <repo>/bundle/paintsville/site. Renders 18 pages + sitemap/robots/favicon/manifest/main.css,
                     copies assets/img, then runs check_site (warnings only; always exits 0).
  site_lib.py        constants (phone, hours, booking URL, form id …), CSS, page shell, components, JSON-LD helpers
  content.py         all copy as data: services, prices (from the price sheet), FAQs, provider bios, specials
  check_site.py      QA: one H1, title <= 60, description 120-155, canonical, JSON-LD parses, forbidden phrases,
                     broken internal links, missing images (incl. srcset), alt text. Non-fatal inside gen_site.
  nginx.conf         config for the paintsville-site container (www -> apex 301, gzip, 404, cache headers)
  DEPLOY-SNIPPETS.md exactly what to add to serenemain's build.sh, docker-compose.yml, deploy.sh and .gitignore
  assets/img/        source images (<= 1600px, jpg q82) + logos/ + badges/ + 800/ (pre-generated srcset variants)
  _standalone/       build.sh / deploy.sh / docker-compose.yml for running this site on its own — NOT used by serenemain
```

## Constants to confirm (`site_lib.py`, marked `TODO(Robin)`)

| Constant | Current value | Notes |
|---|---|---|
| `PHONE` | `(606) 963-0001` | confirmed; drives tel: links and JSON-LD |
| `HOURS` / `HOURS_LD` | `Mon–Fri 9:00 AM – 5:00 PM` / `Mo-Fr 09:00-17:00` | confirmed; keep both in sync |
| `BOOK_URL` | `https://www.vagaro.com/serenemedspapaintsville` | TODO — every "Book Online" button |
| `JOTFORM_ID` | `TODO` | set the form id and /contact/ swaps the phone/email fallback for the embedded Jotform |
| `GBP_REVIEW_URL` | `TODO` | Google "write a review" link; until set, review CTAs point to /contact/#review |
| `GA4_ID`, `META_PIXEL_ID` | empty | tags are only emitted when filled in |
| `GEO` | 37.8145, -82.8071 | approximate; copy the exact pin from Google Business Profile |

Other edits:
* **Prices** — `content.py` → `PRICES` (the /pricing/ page) and each service's `prices` list. Keep them in sync.
* **Specials** — `content.py` → `SPECIALS`; an empty list shows the "coming soon" placeholder.
* **Copy / FAQs / bios** — `content.py`. Titles <= 60 chars, descriptions 120–155 (check_site warns otherwise).
* **Compliance** — never "vaginal rejuvenation", "permanent" hair removal, "laser lipo", or drug names; check_site flags them.
* **Images** — drop a <= 1600px jpg in `assets/img/`, make an 800px copy in `assets/img/800/` (same filename), reference
  it as `/img/name.jpg` through `site_lib.img()`. If Pillow is installed locally, gen_site creates a missing 800 variant
  for you (then commit it).

## Build & preview

```
python3 paintsville/gen_site.py                    # -> bundle/paintsville/site
cd bundle/paintsville/site && python3 -m http.server 8080
```

## Deploy
Handled by serenemain's existing auto-push + VPS autodeploy once the snippets in `DEPLOY-SNIPPETS.md` are added.
The site is served by container `paintsville-site` (nginx:alpine) for `serenemedspaky.com` + `www` via traefik.
