# -*- coding: utf-8 -*-
"""deals_page.py — /deal-of-the-day/ (one deal per office per day, sold as a Mangomint gift-card promotion).

Data: deals_data/deals_*.json  [{date, office, treatment, covers, regular, price, off}]
      deals_data/glow_*.json   {date: {joke, myth:{q,a,why}}}
Live sold-out state: GET /api/deals/status (deals_api/app.py). If that endpoint is unreachable the page simply shows
the deal as available; staff can still end the promotion in Mangomint.
"""
import os, json, glob
from site_lib import *

HERE = os.path.dirname(os.path.abspath(__file__))
GIFT_URL = "https://clients.mangomint.com/gift-cards/serenemedspa"
OFFICE_NAMES = {"hudson": "Hudson, OH", "barboursville": "Barboursville, WV"}

def _load():
    deals, glow = [], {}
    for f in sorted(glob.glob(os.path.join(HERE, "deals_data", "deals_*.json"))): deals += json.load(open(f, encoding="utf-8"))
    for f in sorted(glob.glob(os.path.join(HERE, "deals_data", "glow_*.json"))): glow.update(json.load(open(f, encoding="utf-8")))
    return deals, glow

def promo_name(d):
    import datetime as _dt
    dt = _dt.date.fromisoformat(d["date"])
    return f'{"Hudson" if d["office"] == "hudson" else "Barboursville"} Deal · {dt.strftime("%b")} {dt.day} · {d["treatment"]}'

def deal_of_day():
    deals, glow = _load()
    for d in deals: d["promo"] = promo_name(d)
    data = json.dumps({"deals": deals, "glow": glow, "gift": GIFT_URL,
                       "book": {"hudson": HUDSON["book"], "barboursville": BARB["book"]}}, ensure_ascii=False).replace("</", "<\\/")
    body = page_hero("Deal of the Day", "One treatment. One price. One available per office. A new deal drops every night at midnight &mdash; when it&rsquo;s gone, it&rsquo;s gone.",
                     [("/", "Home"), ("/specials/", "Specials"), (None, "Deal of the Day")], "Hudson, OH &middot; Barboursville, WV") + '''
<style>
.dotd-bar{display:flex;flex-wrap:wrap;gap:10px 24px;align-items:center;justify-content:center;margin:0 auto 26px;font-size:.95rem;color:var(--ink-soft)}
.dotd-clock{font-family:'Poppins',sans-serif;font-weight:600;font-size:1.35rem;color:var(--teal-900);letter-spacing:.04em}
.dotd{display:flex;flex-direction:column;border-top:4px solid var(--sage);position:relative}
.dotd h3{font-size:1.75rem;margin:6px 0 6px;color:var(--teal-900)}
.dotd .covers{color:var(--ink-soft);margin:0 0 16px}
.dotd .price{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;margin:0 0 6px}
.dotd .price s{color:#8a9296;font-size:1.1rem}
.dotd .price b{font-family:'Poppins',sans-serif;font-size:2.4rem;color:var(--teal-900);line-height:1}
.dotd .pill{background:var(--rose);color:#fff;border-radius:30px;padding:4px 12px;font-size:.75rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.dotd .left{font-size:.8rem;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:var(--teal-500);margin:8px 0 16px}
.dotd .how{font-size:.85rem;color:var(--ink-soft);margin-top:12px}
.dotd.sold .buy{display:none}
.dotd .soldout{display:none;font-family:'Poppins',sans-serif;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:var(--teal-900);border-radius:40px;padding:15px 20px;text-align:center}
.dotd.sold .soldout{display:block}
.dotd.sold .price b{text-decoration:line-through;opacity:.45}
.glow{max-width:760px;margin:0 auto;text-align:center}
.glow .joke{font-size:1.35rem;line-height:1.5;color:var(--teal-900);margin:8px 0 26px}
.glow .myth{background:#fff;border-radius:18px;padding:22px 24px;box-shadow:var(--shadow)}
.glow .myth p{margin:6px 0}
.glow .answer{display:none;margin-top:12px}
.glow .answer b{color:var(--teal-900)}
.glow.revealed .answer{display:block}
.glow.revealed .reveal-btn{display:none}
.fine{font-size:.88rem;color:var(--ink-soft);max-width:820px;margin:26px auto 0}
</style>
<section><div class="wrap">
  <div class="dotd-bar"><span id="dotd-date"></span><span>New deals in <span class="dotd-clock" id="dotd-clock">--:--:--</span></span></div>
  <div class="grid g2" id="dotd-cards"></div>
  <p class="fine" id="dotd-fine">One available per office per day, one per person. Each deal is sold as a Serene Med Spa gift card loaded with the treatment&rsquo;s full regular value, to use at the office named in the deal. Treatment is provided only if it&rsquo;s appropriate after your consultation with our provider. If you&rsquo;re not a candidate, you choose: a full refund of what you paid, or keep the gift card at its full value toward any other service or product. Please book your deal treatment within 60 days; the gift card itself never expires. If a deal is ever oversold, you&rsquo;ll get a full refund or we&rsquo;ll honor the deal. Can&rsquo;t be combined with another discount. Gift card purchases are processed securely by Mangomint.</p>
</div></section>
<section class="tint-sand"><div class="wrap">
  <div class="glow" id="glow">
    <span class="eyebrow">The Daily Glow</span>
    <p class="joke" id="glow-joke"></p>
    <div class="myth"><p style="font-size:.8rem;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--teal-500)">Skin myth or fact?</p>
      <p id="glow-q" style="font-size:1.15rem"></p>
      <button class="btn btn-sm reveal-btn" type="button" onclick="document.getElementById('glow').classList.add('revealed')">Reveal the answer</button>
      <p class="answer"><b id="glow-a"></b> &mdash; <span id="glow-why"></span></p></div>
    <p style="margin-top:22px;font-size:.9rem;color:var(--ink-soft)">A new joke and a new myth every day. Come back tomorrow.</p>
  </div>
</div></section>
<script id="dotd-data" type="application/json">''' + data + '''</script>
<script>
(function(){
  var D = JSON.parse(document.getElementById('dotd-data').textContent);
  var NAMES = {hudson:'Hudson, OH', barboursville:'Barboursville, WV'};
  function et(){ var p={}; new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',hour:'2-digit',minute:'2-digit',second:'2-digit',hour12:false}).formatToParts(new Date()).forEach(function(x){p[x.type]=x.value});
    return {date:p.year+'-'+p.month+'-'+p.day, h:+p.hour%24, m:+p.minute, s:+p.second}; }
  var today = et().date, first = D.deals.length ? D.deals[0].date : null;
  var todays = D.deals.filter(function(d){return d.date===today});
  var pretty = new Date(today+'T12:00:00').toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric'});
  document.getElementById('dotd-date').textContent = pretty;
  var cards = document.getElementById('dotd-cards');
  function money(n){return '$'+n.toLocaleString('en-US')}
  function esc(s){var e=document.createElement('span');e.textContent=s;return e.innerHTML}
  if (todays.length){
    todays.sort(function(a,b){return a.office<b.office?1:-1});
    cards.innerHTML = todays.map(function(d){ return '<div class="card dotd reveal visible" data-office="'+d.office+'">'+
      '<span class="eyebrow">'+NAMES[d.office]+'</span><h3>'+esc(d.treatment)+'</h3><p class="covers">'+esc(d.covers)+'</p>'+
      '<div class="price"><s>'+money(d.regular)+'</s><b>'+money(d.price)+'</b><span class="pill">'+d.off+'% off</span></div>'+
      '<p class="left">Only 1 available today</p>'+
      '<a class="btn buy" href="'+D.gift+'" target="_blank" rel="noopener">Buy now</a><div class="soldout">Sold out &mdash; new deal at midnight</div>'+
      '<p class="how">On the next screen, choose <strong>&ldquo;'+esc(d.promo)+'&rdquo;</strong>, then book your visit at the '+NAMES[d.office]+' office.</p></div>'; }).join('');
  } else if (first && today < first){
    cards.innerHTML = '<div class="card dotd" style="grid-column:1/-1;text-align:center"><span class="eyebrow">Coming October 1</span><h3>Deal of the Day starts '+new Date(first+'T12:00:00').toLocaleDateString('en-US',{month:'long',day:'numeric'})+'</h3><p class="covers">One treatment a day at each office, one available, at a price you won&rsquo;t see anywhere else. The first deals go live at midnight.</p></div>';
  } else {
    cards.innerHTML = '<div class="card dotd" style="grid-column:1/-1;text-align:center"><span class="eyebrow">Stay tuned</span><h3>New deals are on the way</h3><p class="covers">In the meantime, see <a href="/specials/">this month&rsquo;s specials</a>.</p></div>';
  }
  function tick(){ var t=et(); var left=(23-t.h)*3600+(59-t.m)*60+(60-t.s); if(left<=0||t.date!==today){location.reload();return}
    var h=Math.floor(left/3600), m=Math.floor(left%3600/60), s=left%60; document.getElementById('dotd-clock').textContent=h+':'+(m<10?'0':'')+m+':'+(s<10?'0':'')+s; }
  tick(); setInterval(tick,1000);
  function poll(){ if(!todays.length) return; fetch('/api/deals/status',{cache:'no-store'}).then(function(r){return r.ok?r.json():null}).then(function(s){
      if(!s||s.date!==today) return; document.querySelectorAll('.dotd[data-office]').forEach(function(c){ c.classList.toggle('sold', !!(s[c.dataset.office]&&s[c.dataset.office].sold)); }); }).catch(function(){}); }
  poll(); setInterval(poll,30000);
  var g = D.glow[today] || D.glow[first] || null;
  if (g){ document.getElementById('glow-joke').textContent=g.joke; document.getElementById('glow-q').textContent=g.myth.q; document.getElementById('glow-a').textContent=g.myth.a; document.getElementById('glow-why').textContent=g.myth.why; }
  else document.getElementById('glow').style.display='none';
})();
</script>'''
    return shell("/deal-of-the-day/", "Deal of the Day | Serene Med Spa", "One med spa treatment a day at each office, Hudson, OH and Barboursville, WV. One available, deep discount, new deal every midnight. Plus the Daily Glow.", body)

def specials_banner():
    return '''<section style="padding-bottom:0"><div class="wrap"><div class="card" style="display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center;justify-content:space-between;border-top:4px solid var(--rose)">
  <div><span class="eyebrow">New &middot; starts October 1</span><h3 style="margin:6px 0 4px">Deal of the Day</h3><p style="margin:0;color:var(--ink-soft)">One treatment a day at each office, one available, new deal every midnight.</p></div>
  <a class="btn" href="/deal-of-the-day/">See today&rsquo;s deals</a></div></div></section>'''
