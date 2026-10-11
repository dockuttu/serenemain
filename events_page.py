# /events/inbody-open-house/ - free InBody open house, Mon Nov 2 2026, 4-7 PM, both offices (Robin, Oct 10 2026).
# RSVP = Jotform 262828603340051 (name, email, mobile, office, party size, arrival window, optional marketing consent).
from site_lib import shell, page_hero, HUDSON, BARB

RSVP = "https://form.jotform.com/262828603340051"

def open_house():
    body = page_hero("Free InBody Open House", "Monday, November 2, 4&ndash;7 PM at both Serene Med Spa offices. Free InBody 580 body-composition scans, short talks from our physician-led team, light refreshments and a raffle for a free HydraFacial.",
                     [("/", "Home"), ("/inbody-body-scan/", "Free InBody scan"), (None, "Open house")], "You&rsquo;re invited") + f'''
<section><div class="wrap" style="display:grid;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:36px;align-items:start">
  <div class="prose">
    <h2>What to expect</h2>
    <ul>
      <li><strong>Free InBody scan</strong> in about a minute: muscle, body fat and body water, with a printout to keep</li>
      <li><strong>Short talks at 4:30 and 6:00 PM:</strong> &ldquo;Fat or muscle? How to read your InBody results&rdquo;</li>
      <li><strong>Meet the team</strong>, tour the office and ask questions, with free consultations on the night</li>
      <li><strong>Raffle:</strong> one free Signature HydraFacial at each office</li>
      <li>Sparkling water, mocktails and light snacks</li>
    </ul>
    <h2>Where</h2>
    <p><strong>Hudson:</strong> {HUDSON["addr1"]}, {HUDSON["addr2"]} &middot; text <a data-txt href="sms:{HUDSON["sms"]}">{HUDSON["text"]}</a><br>
       <strong>Barboursville:</strong> {BARB["addr1"]}, {BARB["addr2"]} &middot; text <a data-txt href="sms:{BARB["sms"]}">{BARB["text"]}</a></p>
    <h2>Before your scan</h2>
    <p>Don&rsquo;t eat for 2&ndash;3 hours before, skip lotion on your hands and feet, and plan to take off your shoes and socks. InBody scans aren&rsquo;t for anyone with a pacemaker or other implanted electronic device; if you&rsquo;re pregnant, text us first.</p>
    <p style="font-size:.85rem;color:var(--muted)"><strong>Raffle rules:</strong> one free Signature HydraFacial per office (value $150). One entry per adult 18 or older who attends. No purchase, review or social post is needed to enter or win. Drawn at 6:45 PM; the winner doesn&rsquo;t need to be present and is notified by text. Redeem by February 28, 2027. Not exchangeable for cash; can&rsquo;t be combined with another discount.</p>
  </div>
  <div style="background:#fff;border:1px solid rgba(30,74,85,.14);border-radius:16px;padding:8px;box-shadow:0 10px 30px rgba(27,42,47,.06)">
    <iframe title="RSVP for the free InBody open house" src="{RSVP}" loading="lazy" style="width:100%;min-height:1050px;border:0;display:block"></iframe>
  </div>
</div></section>
<style>@media(max-width:860px){{section .wrap[style*="grid-template-columns"]{{grid-template-columns:1fr!important}}}}</style>'''
    return shell("/events/inbody-open-house/", "Free InBody Open House, Mon Nov 2 | Serene Med Spa Hudson & Barboursville",
                 "Free open house Monday, November 2, 4-7 PM at Serene Med Spa in Hudson, OH and Barboursville, WV: free InBody scans, short talks and a HydraFacial raffle. RSVP.",
                 body, og_image="/img/social/inbody/inbody-hero.jpg")
