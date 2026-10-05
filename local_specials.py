"""local_specials.py: ONE source of truth for the office specials block that sits right under the featured video on
serenemedspas.com/ (main home), /hudson/ and /barboursville/ (Robin, Oct 5 2026: "the main domain and 2 locations are not in sync").

Edit OFFERS below and push serenemain: the main deploy rebuilds the Hudson and Barboursville sites too (see deploy.sh),
so all three home pages show the same offers. Each card shows itself only between its from/until dates (Eastern time),
and the Deal of the Day card reads deals_data/deals_*.json, so day-to-day changes need no edits at all.

Used by: site_lib.local_specials_section(office) -> pages_custom.home() (office=None: follows the visitor's chosen
location, or shows both offices), serenehudson/v2_merge.py (office="hudson"), serenebarboursville/v2_merge.py ("barboursville").
"""
import datetime as _d, glob as _glob, json as _json, os as _os

HERE = _os.path.dirname(_os.path.abspath(__file__))
GIFT = "https://clients.mangomint.com/gift-cards/serenemedspa"
OFFICE_NAME = {"hudson": "Hudson", "barboursville": "Barboursville"}

# items: either a list (same for both offices) or {"hudson": [...], "barboursville": [...]}.
# buttons: (label, href); href "BOOK" = that office's online booking, "{o}" in an href = the office slug.
OFFERS = [
    {"id": "ultherapy-oct", "offices": ["hudson", "barboursville"], "from": "2026-10-01", "until": "2026-10-31",
     "eyebrow": "Through October 31 &middot; first 20 clients", "title": "30% off Ultherapy PRIME",
     "items": {"hudson": ["Non-surgical ultrasound lift for brow, jowls, neck and d&eacute;collet&eacute;",
                          "Regular: brow $950 &middot; lower face $1,900 &middot; full face $2,600, now 30% off"],
               "barboursville": ["Non-surgical ultrasound lift for brow, jowls, neck and d&eacute;collet&eacute;",
                                 "Regular: brow $850 &middot; lower face $1,650 &middot; full face $2,200, now 30% off"]},
     "note": "As seen on WSAZ Studio 3 &middot; mention &ldquo;Studio 3&rdquo;",
     "buttons": [("Book a consult", "BOOK"), ("Ultherapy pricing", "/{o}/ultherapy/#pricing")]},
    {"id": "fall-laser-oct", "offices": ["barboursville"], "from": "2026-10-01", "until": "2026-10-31",
     "eyebrow": "Through October 31", "title": "Fall Laser Season",
     "items": ["<strong>BBL + MOXI, same visit: $750</strong> (regularly $900)", "<strong>BBL HEROic:</strong> buy 3, get 1 free",
               "<strong>Laser hair removal:</strong> buy 5, get 2 free"],
     "note": "Can&rsquo;t be combined with another discount",
     "buttons": [("Book Now", "BOOK"), ("About MOXI", "/barboursville/sciton-moxi/")]},
    {"id": "giftcard-holiday", "offices": ["hudson", "barboursville"], "from": "2026-11-01", "until": "2026-12-24",
     "eyebrow": "Through December 24", "title": "Holiday gift card bonus",
     "items": ["<strong>$225 gift card for $200</strong>", "<strong>$575 gift card for $500</strong>"],
     "note": "Black Friday weekend (Nov 27&ndash;30) the bonus doubles &middot; gift cards never expire",
     "buttons": [("Buy a gift card", GIFT), ("Details", "/specials/#holiday")]},
    {"id": "black-friday", "offices": ["hudson", "barboursville"], "from": "2026-11-27", "until": "2026-11-30",
     "eyebrow": "Black Friday weekend &middot; Nov 27&ndash;30", "title": "Prepaid Black Friday savings",
     "items": {"hudson": ["<strong>Double gift card bonus:</strong> $250 card for $200, $650 for $500",
                          "<strong>50 units of Botox or Xeomin:</strong> $450 prepaid", "<strong>3 syringes of Juv&eacute;derm:</strong> $1,200",
                          "<strong>20% off</strong> any prepaid series of 3"],
               "barboursville": ["<strong>Double gift card bonus:</strong> $250 card for $200, $650 for $500",
                                 "<strong>50 units of Botox or Xeomin:</strong> $400 prepaid", "<strong>3 syringes of Juv&eacute;derm:</strong> $1,200",
                                 "<strong>20% off</strong> any prepaid series of 3"]},
     "note": "Prepaid Nov 27&ndash;30, use within 12 months",
     "buttons": [("Shop Black Friday", "/specials/#black-friday")]},
    {"id": "party-glow-dec", "offices": ["hudson", "barboursville"], "from": "2026-12-01", "until": "2026-12-19",
     "eyebrow": "December 1&ndash;19", "title": "Party-ready glow: 15% off",
     "items": ["<strong>HydraFacial</strong>, glowing skin the same day", "<strong>VI Peel</strong>, book a week or two before your event"],
     "note": "Can&rsquo;t be combined with another discount",
     "buttons": [("Book Now", "BOOK")]},
    {"id": "newyear-prepay", "offices": ["hudson", "barboursville"], "from": "2026-12-26", "until": "2026-12-31",
     "eyebrow": "December 26&ndash;31", "title": "New Year prepay: 15% off",
     "items": ["Prepay <strong>any series of 3</strong> and save 15%"],
     "note": "Use within 12 months",
     "buttons": [("See all specials", "/specials/")]},
]


def _deals(days_back=2, days_ahead=75):
    out = []
    for f in sorted(_glob.glob(_os.path.join(HERE, "deals_data", "deals_*.json"))):
        try:
            out += _json.load(open(f, encoding="utf-8"))
        except Exception:
            pass
    lo = (_d.date.today() - _d.timedelta(days=days_back)).isoformat()
    hi = (_d.date.today() + _d.timedelta(days=days_ahead)).isoformat()
    keep = ("date", "office", "treatment", "covers", "regular", "price")
    return [{k: x.get(k) for k in keep} for x in out if x.get("office") in OFFICE_NAME and lo <= x.get("date", "") <= hi]


def _resolved_offers(book):
    res = []
    for o in OFFERS:
        if o["until"] < (_d.date.today() - _d.timedelta(days=1)).isoformat():
            continue  # expired: keep the page small
        for off in o["offices"]:
            items = o["items"][off] if isinstance(o["items"], dict) else o["items"]
            btns = [(lbl, book[off] if href == "BOOK" else href.replace("{o}", off)) for lbl, href in o["buttons"]]
            res.append({"id": o["id"], "office": off, "offices": o["offices"], "from": o["from"], "until": o["until"],
                        "eyebrow": o["eyebrow"], "title": o["title"], "items": items, "note": o.get("note", ""), "buttons": btns})
    return res


CSS = ('#loc-specials .ls-grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));max-width:1100px;margin:0 auto}'
       '#loc-specials .card{display:flex;flex-direction:column;border-top:4px solid var(--sage,#6F9A8F)}'
       '#loc-specials .card h3{margin:6px 0 8px;color:var(--forest,#10322F)}'
       '#loc-specials ul{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:10px}'
       '#loc-specials li{padding-left:22px;position:relative}#loc-specials li::before{content:"";position:absolute;left:0;top:.5em;width:10px;height:10px;border-radius:50%;background:var(--sage,#6F9A8F)}'
       '#loc-specials .ls-price{display:flex;align-items:baseline;gap:10px;margin:4px 0 6px}#loc-specials .ls-price s{color:#8a9296}'
       '#loc-specials .ls-price b{font-family:Poppins,sans-serif;font-size:2.1rem;color:var(--forest,#10322F);line-height:1}'
       '#loc-specials .ls-note{margin-top:auto;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;color:var(--forest-500,#3E7F78);font-weight:600}'
       '#loc-specials .ls-actions{margin-top:14px;display:flex;flex-wrap:wrap;gap:8px}'
       '#loc-specials .ls-tag{display:inline-block;font-size:.66rem;letter-spacing:.16em;text-transform:uppercase;font-weight:600;background:var(--lav-100,#eceefa);color:var(--forest,#10322F);border-radius:30px;padding:4px 10px;margin-bottom:6px}'
       '#loc-specials .ls-dotd{margin-top:56px;padding-top:44px;border-top:1px solid #e6e0d8}'
       '#loc-specials .ls-dhead{display:flex;align-items:center;justify-content:center;gap:18px;text-align:center}'
       '#loc-specials .ls-dhead img{width:96px;height:60px;flex:0 0 auto}'
       '#loc-specials .ls-dhead h2{margin:4px 0 0}'
       '#loc-specials .ls-new{display:block;font-size:.74rem;letter-spacing:.18em;text-transform:uppercase;font-weight:700;color:#d23c3c}'
       '#loc-specials .ls-dintro{text-align:center;max-width:620px;margin:14px auto 24px;color:var(--ink-soft,#555)}'
       '#loc-specials .ls-dgrid{display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(280px,420px));justify-content:center}'
       '#loc-specials .ls-dcard{border-top-color:#d23c3c}'
       '@media (max-width:560px){#loc-specials .ls-dhead img{width:56px;height:35px}#loc-specials .ls-dhead{gap:8px}}'
       '#loc-specials .section-head{text-align:center;max-width:none;margin-left:auto;margin-right:auto}#loc-specials .section-head h2{margin-left:auto;margin-right:auto}#loc-specials .ls-more{text-align:center;margin-top:22px}')

# Renders in the browser from the embedded JSON: picks today's date in Eastern time, the office (fixed on /hudson/ and
# /barboursville/; on the main home it follows the saved location, or shows both offices with a tag on each card).
JS = r"""<script>(function(){try{
var S=document.getElementById('loc-specials');if(!S)return;var C=JSON.parse(document.getElementById('ls-data').textContent);
var t=new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York'}).format(new Date());
var M=['January','February','March','April','May','June','July','August','September','October','November','December'];
function esc(x){return String(x==null?'':x).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function office(){if(C.office)return C.office;var k='';try{k=localStorage.getItem('serene_loc')||'';}catch(e){}return (k==='hudson'||k==='barboursville')?k:'';}
function render(){var o=office(),both=!o,N={hudson:'Hudson',barboursville:'Barboursville'},h='',dh='';
 var offs=both?['hudson','barboursville']:[o];
 offs.forEach(function(of){var d=null;C.deals.forEach(function(x){if(x.office===of&&x.date===t)d=x;});if(!d)return;
  dh+='<div class="card ls-dcard" data-dotd="'+of+'">'+'<span class="eyebrow">'+(both?N[of]+' &middot; ':'')+'Today only</span><h3>'+esc(d.treatment)+'</h3>'
   +'<p style="color:var(--ink-soft);margin:0 0 10px">'+esc(d.covers||'')+'</p><div class="ls-price"><s>$'+esc(d.regular)+'</s><b>$'+esc(d.price)+'</b></div>'
   +'<p class="ls-note ls-left" style="margin-top:6px">Only 1 available &middot; new deal every midnight</p>'
   +'<div class="ls-actions"><a class="btn ls-buy" href="/deal-of-the-day/">Get today&rsquo;s deal</a></div></div>';});
 var seen={};C.offers.forEach(function(x){if(t<x.from||t>x.until)return;if(offs.indexOf(x.office)<0)return;
  if(both&&x.offices.length>1){if(seen[x.id])return;seen[x.id]=1;}
  var tag=both?(x.offices.length>1?'Hudson &amp; Barboursville':N[x.office]+' only'):'';
  var items=(both&&x.offices.length>1)?x.items.filter(function(i){return !/^Regular:/.test(i);}):x.items;
  h+='<div class="card">'+(tag?'<span class="ls-tag">'+tag+'</span>':'')+'<span class="eyebrow">'+x.eyebrow+'</span><h3>'+x.title+'</h3><ul>'
   +items.map(function(i){return '<li>'+i+'</li>';}).join('')+'</ul>'+(x.note?'<p class="ls-note">'+x.note+'</p>':'')+'<div class="ls-actions">'
   +x.buttons.map(function(b,i){var href=b[1];if(both&&x.offices.length>1&&/booking\.mangomint|\/(hudson|barboursville)\//.test(href)){href=/booking\.mangomint/.test(href)?'/#book':'/specials/';}
     var ext=/^https?:/.test(href);return '<a class="btn'+(i?' btn-outline':'')+'" href="'+href+'"'+(ext?' target="_blank" rel="noopener"':'')+'>'+b[0]+'</a>';}).join('')+'</div></div>';});
 var g=S.querySelector('.ls-grid');g.innerHTML=h;g.style.display=h?'':'none';var D=S.querySelector('.ls-dotd');D.querySelector('.ls-dgrid').innerHTML=dh;D.style.display=dh?'':'none';S.style.display=(h||dh)?'':'none';
 var hd=S.querySelector('[data-ls-month]');if(hd)hd.textContent=M[+t.slice(5,7)-1]+' specials'+(both?' at Serene':' in '+N[o]);
 var e=S.querySelector('[data-ls-eyebrow]');if(e)e.textContent=both?'This month at both offices':'This month at Serene '+N[o];
 if(dh)fetch('/api/deals/status',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(s){if(!s||s.date!==t)return;
  S.querySelectorAll('[data-dotd]').forEach(function(c){var of=c.getAttribute('data-dotd');if(s[of]&&s[of].sold){c.querySelector('.ls-left').textContent='Sold out today · a new deal drops at midnight';var b=c.querySelector('.ls-buy');if(b)b.textContent='See Deal of the Day';}});}).catch(function(){});
}
render();if(!C.office)document.addEventListener('serene:loc',render);
}catch(e){}})();</script>"""

MARK = ("<!--loc-specials-->", "<!--/loc-specials-->")


def section(office=None, book=None):
    """office: 'hudson' | 'barboursville' | None (main home). book: {office: booking URL}."""
    book = book or {}
    data = {"office": office or "", "offers": _resolved_offers(book), "deals": _deals()}
    blob = _json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (MARK[0] + '<section id="loc-specials" style="display:none"><div class="wrap">'
            '<div class="section-head reveal"><span class="eyebrow" data-ls-eyebrow>This month at Serene</span><h2 data-ls-month>This month&rsquo;s specials</h2></div>'
            '<div class="ls-grid"></div>'
            '<p class="ls-more"><a class="btn btn-outline" href="/specials/">All specials</a></p>'
            '<div class="ls-dotd" style="display:none"><div class="ls-dhead"><img src="/img/email/deal-beacon.gif" alt="" width="96" height="60">'
            '<div><span class="ls-new">New deal every midnight</span><h2>Deal of the Day</h2></div><img src="/img/email/deal-beacon.gif" alt="" width="96" height="60"></div>'
            '<p class="ls-dintro">Every day each office puts one treatment on sale, and only one is available. When it&rsquo;s gone, it&rsquo;s gone.</p>'
            '<div class="ls-dgrid"></div><p class="ls-more"><a class="btn" href="/deal-of-the-day/">See today&rsquo;s deals</a></p></div>'
            '<script type="application/json" id="ls-data">' + blob + '</script><style>' + CSS + '</style>' + JS +
            '</div></section>' + MARK[1] + '\n')


def inject_after_video(html, office, book):
    """Idempotent: remove any earlier copy (and the old Barboursville-only block), then place it right after the
    featured video section (id="studio3"), or before the hero once the video has retired."""
    import re
    html = re.sub(re.escape(MARK[0]) + r'.*?' + re.escape(MARK[1]) + r'\n?', "", html, flags=re.S)
    html = re.sub(r'<!--bv-specials-->.*?<!--/bv-specials-->\n?', "", html, flags=re.S)
    blk = section(office, book)
    i = html.find('id="studio3"')
    if i != -1:
        j = html.find('</section>', i)
        if j != -1:
            j += len('</section>')
            return html[:j] + "\n" + blk + html[j:]
    return html.replace('<section class="hero">', blk + '<section class="hero">', 1)
