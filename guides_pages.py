# /guides/ and /guides/<slug>/ - free downloadable guides (lead magnets for ads), Robin, Oct 10 2026.
# Each guide page embeds its HIPAA Jotform (name, email, mobile, office, consent); the thank-you page and the autoresponder
# email give the PDF link (/media/guides/serene-guide-<slug>.pdf, disallowed in robots.txt). No ad/analytics trackers on
# /guides/ pages (site_lib strips them). Content JSON + PDF builder live in the session scratchpad (build_guides.py).
import json, os
from site_lib import shell, page_hero, esc

_HERE = os.path.dirname(os.path.abspath(__file__))
GUIDES = json.load(open(os.path.join(_HERE, "guides_data.json"), encoding="utf-8"))

CSS = """<style>
.gd-grid{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:36px;align-items:start}
.gd-cover{width:100%;max-width:420px;border-radius:10px;box-shadow:0 18px 50px rgba(16,50,47,.18);display:block}
.gd-inside{margin:22px 0 0;padding:0;list-style:none}
.gd-inside li{padding:8px 0 8px 26px;border-bottom:1px solid rgba(30,74,85,.12);position:relative;font-size:.97rem}
.gd-inside li::before{content:"\\2713";position:absolute;left:0;color:var(--teal-500,#3E8FA0);font-weight:700}
.gd-form{background:#fff;border:1px solid rgba(30,74,85,.14);border-radius:16px;padding:8px;box-shadow:0 10px 30px rgba(27,42,47,.06)}
.gd-form iframe{width:100%;min-height:980px;border:0;display:block}
.gd-fine{font-size:.85rem;color:var(--muted,#7C8A8F);margin-top:10px}
.gd-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px}
.gd-card{display:block;background:#fff;border:1px solid rgba(30,74,85,.12);border-radius:14px;overflow:hidden;color:inherit;text-decoration:none;box-shadow:0 8px 24px rgba(27,42,47,.06)}
.gd-card img{width:100%;display:block;aspect-ratio:8.5/11;object-fit:cover}
.gd-card div{padding:14px 16px}
.gd-card h3{font-size:1.02rem;margin:0 0 4px}
@media(max-width:860px){.gd-grid{grid-template-columns:1fr}.gd-cover{max-width:300px;margin:0 auto}}
</style>"""

def guide_page(g):
    inside = "".join(f"<li>{esc(h)}</li>" for h in g["inside"])
    body = page_hero(esc(g["title"]), esc(g["subtitle"]), [("/", "Home"), ("/guides/", "Free guides"), (None, esc(g["title"].split(":")[0]))], "Free guide") + f'''
<section><div class="wrap gd-grid">
  <div><img class="gd-cover" src="/img/guides/guide-cover-{g["slug"]}.jpg" alt="Cover of the free Serene Med Spa guide: {esc(g["title"])}" width="935" height="1210">
    <h2 style="margin-top:26px;font-size:1.35rem">What&rsquo;s inside</h2><ul class="gd-inside">{inside}<li>Prices at our Hudson and Barboursville offices</li><li>A consultation checklist and answers to common questions</li></ul></div>
  <div><div class="gd-form"><iframe title="Request the free guide: {esc(g["title"])}" src="https://form.jotform.com/{g["form"]}" loading="lazy" allow="geolocation; microphone; camera"></iframe></div>
    <p class="gd-fine">Your download link appears as soon as you submit, and we email you a copy. Your information is kept private and secure, and you can opt out of messages at any time. Educational guide, not medical advice.</p></div>
</div></section>'''
    return shell(f"/guides/{g['slug']}/", f"Free Guide: {g['title']} | Serene Med Spa",
                 f"Download our free guide: {g['subtitle']}"[:155], body, og_image=f"/img/guides/guide-cover-{g['slug']}.jpg", extra_head=CSS)

def hub():
    cards = "".join(f'<a class="gd-card" href="/guides/{g["slug"]}/"><img src="/img/guides/guide-cover-{g["slug"]}.jpg" alt="" loading="lazy"><div><h3>{esc(g["title"])}</h3><p style="font-size:.9rem;margin:0">{esc(g["subtitle"])}</p></div></a>' for g in GUIDES)
    body = page_hero("Free guides from our physician-led team", "Straight answers about popular treatments: how they work, who they suit, what to expect and what they cost at Serene. Free to download.",
                     [("/", "Home"), (None, "Free guides")], "Free downloads") + f'<section><div class="wrap"><div class="gd-cards">{cards}</div></div></section>'
    return shell("/guides/", "Free Med Spa Guides | Serene Med Spa", "Free downloadable guides from Serene Med Spa's physician-led team on weight loss, injectables, skin tightening, Ultherapy and perimenopause.", body, extra_head=CSS)

def pages():
    out = {"/guides/": hub()}
    for g in GUIDES:
        out[f"/guides/{g['slug']}/"] = guide_page(g)
    return out
