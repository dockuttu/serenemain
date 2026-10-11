# /inbody-body-scan/ - free InBody 580 body composition scans at both offices from Wed Oct 21, 2026 (Robin, Oct 10 2026).
# Office pages with full detail live at /hudson/inbody-body-scan/ and /barboursville/inbody-body-scan/ (office repos).
# Mangomint service "Free InBody Body Scan" = serviceId 430 (both locations, 15 min, $0, online booking on).
from site_lib import shell, page_hero, HUDSON, BARB

BOOK = "https://booking.mangomint.com/serenemedspa?serviceId=430"

def inbody_page():
    body = page_hero("Free InBody body scan",
                     "Your scale shows one number. An InBody 580 scan shows what&rsquo;s behind it: muscle, body fat and body water, arm by arm and leg by leg. About a minute, a printout to keep, and always free, starting Wednesday, October 21.",
                     [("/", "Home"), ("/service/", "Treatments"), (None, "Free InBody body scan")], "New at both offices") + f'''
<section><div class="wrap">
  <div class="grid g3">
    <div class="card reveal"><span class="eyebrow">Ohio</span><h3>Hudson</h3><p>{HUDSON["addr1"]}<br>{HUDSON["addr2"]}<br><a href="tel:{HUDSON["tel"]}">{HUDSON["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{BOOK}" target="_blank" rel="noopener">Book a free scan</a><a class="btn btn-sm btn-outline" href="/hudson/inbody-body-scan/">Details</a></div></div>
    <div class="card reveal"><span class="eyebrow">West Virginia</span><h3>Barboursville</h3><p>{BARB["addr1"]}<br>{BARB["addr2"]}<br><a href="tel:{BARB["tel"]}">{BARB["phone"]}</a></p><div class="actions"><a class="btn btn-sm" href="{BOOK}" target="_blank" rel="noopener">Book a free scan</a><a class="btn btn-sm btn-outline" href="/barboursville/inbody-body-scan/">Details</a></div></div>
    <div class="card reveal"><span class="eyebrow">What it measures</span><h3>More than weight</h3><p>Skeletal muscle, body fat (pounds and percent), muscle and fat by arm, leg and trunk, visceral fat, body water and an estimate of the calories you burn at rest.</p></div>
  </div>
</div></section>
<section class="tint-sand"><div class="wrap prose">
  <h2>Why it matters</h2>
  <p>Two people can weigh the same and have very different amounts of muscle and fat. When you&rsquo;re losing weight, including on a <a href="/weight-loss/">medical weight-loss program</a>, the scale can&rsquo;t tell you whether you&rsquo;re losing fat, muscle or water. Repeat InBody scans, taken the same way each time, show how your body composition is changing so you can protect muscle while you lose fat.</p>
  <h2>How to prepare</h2>
  <ul>
    <li>Don&rsquo;t eat for 2 to 3 hours before, and use the restroom first.</li>
    <li>Skip exercise, caffeine and alcohol beforehand.</li>
    <li>No lotion on your hands or feet. You&rsquo;ll take off your shoes and socks.</li>
    <li>For the best comparison, scan at the same time of day each visit.</li>
  </ul>
  <p><strong>Please don&rsquo;t book a scan</strong> if you have a pacemaker, defibrillator or other implanted electronic device. If you&rsquo;re pregnant, call us first.</p>
  <p style="font-size:.9rem;color:var(--muted)">Free for everyone, as often as you like, with no purchase required. The scan is a wellness measurement, not a diagnostic test, and it doesn&rsquo;t replace a visit with a clinician. Results are estimates and vary with hydration, food and time of day.</p>
  <div class="actions" style="margin-top:18px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book your free scan</a></div>
</div></section>'''
    return shell("/inbody-body-scan/", "Free InBody Body Scan | Hudson, OH & Barboursville, WV | Serene Med Spa",
                 "Free InBody 580 body composition scans at Serene Med Spa in Hudson, OH and Barboursville, WV, starting October 21. Muscle, body fat and body water in about a minute.",
                 body, og_image="/img/social/inbody/inbody-hero.jpg")
