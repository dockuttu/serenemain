# /events/inbody-open-house/ - free InBody open house (Robin, Oct 10 2026). Oct 13: Robin moved Hudson to Sat Nov 7, 11 AM-2 PM so he can attend both;
# Barboursville stays Mon Nov 2, 4-7 PM.
# RSVP = Jotform 262828603340051 (name, email, mobile, office, party size, arrival window, optional marketing consent).
from site_lib import shell, page_hero, HUDSON, BARB

RSVP = "https://form.jotform.com/262828603340051"

def open_house():
    body = page_hero("Free InBody Open House", "Barboursville: Monday, November 2, 4&ndash;7 PM. Hudson: Saturday, November 7, 11 AM&ndash;2 PM. Free InBody 580 body-composition scans, short talks from our physician-led team, light refreshments and a raffle for a free HydraFacial.",
                     [("/", "Home"), ("/inbody-body-scan/", "Free InBody scan"), (None, "Open house")], "You&rsquo;re invited") + f'''
<section><div class="wrap" style="display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:36px;align-items:start">
  <div class="prose">
    <h2>What to expect</h2>
    <ul>
      <li><strong>Free InBody scan</strong> in about a minute: muscle, body fat and body water, with a printout to keep</li>
      <li><strong>Short talks</strong> (Barboursville 4:30 and 6:00 PM; Hudson 11:30 AM and 1:00 PM): &ldquo;Fat or muscle? How to read your InBody results&rdquo;</li>
      <li><strong>Meet the team</strong>, tour the office and ask questions, with free consultations on the night</li>
      <li><strong>Raffle:</strong> one free Signature HydraFacial at each office</li>
      <li>Sparkling water, mocktails and light snacks</li>
    </ul>
    <h2>Where</h2>
    <p><strong>Barboursville &middot; Mon Nov 2, 4&ndash;7 PM:</strong> {BARB["addr1"]}, {BARB["addr2"]} &middot; text <a data-txt href="sms:{BARB["sms"]}">{BARB["text"]}</a><br>
       <strong>Hudson &middot; Sat Nov 7, 11 AM&ndash;2 PM:</strong> {HUDSON["addr1"]}, {HUDSON["addr2"]} &middot; text <a data-txt href="sms:{HUDSON["sms"]}">{HUDSON["text"]}</a></p>
    <h2>Before your scan</h2>
    <p>Don&rsquo;t eat for 2&ndash;3 hours before, skip lotion on your hands and feet, and plan to take off your shoes and socks. InBody scans aren&rsquo;t for anyone with a pacemaker or other implanted electronic device; if you&rsquo;re pregnant, text us first.</p>
    <p style="font-size:.85rem;color:var(--muted)"><strong>Raffle rules:</strong> one free Signature HydraFacial per office (value $149). One entry per adult 18 or older who attends. No purchase, review or social post is needed to enter or win. Drawn at 6:45 PM in Barboursville and 1:45 PM in Hudson; the winner doesn&rsquo;t need to be present and is notified by text. Redeem by February 28, 2027. Not exchangeable for cash; can&rsquo;t be combined with another discount.</p>
  </div>
  <div style="background:#fff;border:1px solid rgba(30,74,85,.14);border-radius:16px;padding:8px;box-shadow:0 10px 30px rgba(27,42,47,.06)">
    <iframe title="RSVP for the free InBody open house" src="{RSVP}" loading="lazy" style="width:100%;min-height:1050px;border:0;display:block"></iframe>
  </div>
</div></section>
<style>@media(max-width:860px){{section .wrap[style*="grid-template-columns"]{{grid-template-columns:1fr!important}}}}</style>'''
    return shell("/events/inbody-open-house/", "Free InBody Open House: Barboursville Nov 2, Hudson Nov 7 | Serene Med Spa",
                 "Free InBody open house at Serene Med Spa: Barboursville, WV Mon Nov 2, 4-7 PM; Hudson, OH Sat Nov 7, 11 AM-2 PM. Free scans, short talks, HydraFacial raffle. RSVP.",
                 body, og_image="/img/social/inbody/inbody-hero.jpg")
