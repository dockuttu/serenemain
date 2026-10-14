# /weight-loss/brand-name-medications/ - manufacturer self-pay prices for brand-name GLP-1 weight-loss medications,
# prescribed through Serene Telehealth (Robin, Oct 14 2026). Organic info page only: NOT for ads or /lp/ pages,
# no trackers (NO_TRACK_PATHS). Prices from the Novo Nordisk self-pay comparison sheet US26SEMO01665, accurate as of
# Sept 2, 2026 - re-check when the manufacturers change offers (Wegovy pen intro offer ends Dec 31, 2026).
# Ozempic is intentionally NOT listed (diabetes indication, not weight management).
import json
from site_lib import shell, page_hero, TELE, SITE_URL

SLUG = "/weight-loss/brand-name-medications/"
AS_OF = "September 2, 2026"

ROWS = [  # (medication, form, dose, monthly self-pay price, note)
    ("Wegovy&reg;", "Tablets (once daily)", "1.5 mg", "$149", ""),
    ("Wegovy&reg;", "Tablets (once daily)", "4 mg", "$199", ""),
    ("Wegovy&reg;", "Tablets (once daily)", "9 mg or 25 mg", "$299", ""),
    ("Wegovy&reg;", "Pen (weekly injection)", "0.25 mg or 0.5 mg", "$199", "New-patient offer for the first 2 monthly fills, through Dec 31, 2026"),
    ("Wegovy&reg;", "Pen (weekly injection)", "0.25 / 0.5 / 1 / 1.7 / 2.4 mg", "$349", ""),
    ("Wegovy&reg; HD", "Pen (weekly injection)", "7.2 mg", "$399", ""),
    ("Zepbound&reg;", "Vial or pen (weekly injection)", "2.5 mg", "$299", ""),
    ("Zepbound&reg;", "Vial or pen (weekly injection)", "5 mg", "$399", ""),
    ("Zepbound&reg;", "Vial or pen (weekly injection)", "7.5 mg", "$449", "When each refill is filled within 45 days; otherwise $499"),
    ("Zepbound&reg;", "Vial or pen (weekly injection)", "10, 12.5 or 15 mg", "$449", "When each refill is filled within 45 days; otherwise $699"),
    ("Foundayo&reg;", "Tablets (once daily)", "0.8 mg or 2.5 mg", "$149", ""),
    ("Foundayo&reg;", "Tablets (once daily)", "5.5 mg", "$199", ""),
    ("Foundayo&reg;", "Tablets (once daily)", "9 mg", "$299", ""),
    ("Foundayo&reg;", "Tablets (once daily)", "14.5 or 17.2 mg", "$299", "When each refill is filled within 45 days; otherwise $349"),
]

FAQ = [
    ("Do I need insurance?", "No. These are the manufacturers&rsquo; cash prices for people who pay out of pocket. If your insurance covers weight-loss medication, using it may cost you less; we can send the prescription to your regular pharmacy instead."),
    ("Who do I pay for the medication?", "You pay the manufacturer&rsquo;s self-pay pharmacy directly, and the medication ships to your home. Serene does not sell these medications or receive any part of the payment."),
    ("What does Serene charge?", "Your care is through Serene Telehealth: a flat $149 per month that covers your video visits, follow-ups and secure messaging with Dr. Robin Arora. Medication and any labs are paid separately."),
    ("Will I definitely get a prescription?", "No. Dr. Arora prescribes only when the medication is medically appropriate for you, after reviewing your history, current medications and any labs."),
    ("Which states?", "Telehealth visits are available to patients physically located in Ohio, West Virginia, Kentucky or Florida at the time of the visit. Patients of our Hudson, OH and Barboursville, WV offices are welcome."),
    ("Are the prices guaranteed?", f"No. Prices are set by the manufacturers, were accurate as of {AS_OF}, and can change at any time. Eligibility rules and restrictions apply; government-insured patients may be excluded from some offers."),
]

def brand_glp1_page():
    tel, sms = TELE["tel"], TELE["tel"]
    rows = "".join(
        f'<tr><td><strong>{m}</strong><br><span style="font-size:.85rem;color:var(--muted)">{f}</span></td><td>{d}</td>'
        f'<td style="white-space:nowrap"><strong>{p}</strong>/month</td><td style="font-size:.85rem;color:var(--muted)">{n}</td></tr>'
        for m, f, d, p, n in ROWS)
    faq_html = "".join(f'<div class="card reveal"><h3>{q}</h3><p style="font-size:.97rem">{a}</p></div>' for q, a in FAQ)
    cta = (f'<div class="actions" style="margin:20px 0"><a class="btn" href="sms:{sms}">Text us {TELE["phone"]}</a>'
           f'<a class="btn btn-outline" href="{TELE["spruce"]}" target="_blank" rel="noopener">Start a telehealth visit</a>'
           f'<a class="btn btn-outline" href="tel:{tel}">Call {TELE["phone"]}</a></div>')
    body = page_hero("Brand-name weight-loss medication, prescribed by telehealth",
                     "Prefer the original, FDA-approved brand-name medication? Several manufacturers now sell it directly to self-paying patients at a reduced cash price, delivered to your home. Dr. Robin Arora can evaluate you by video and send the prescription when it&rsquo;s right for you.",
                     [("/", "Home"), ("/weight-loss/", "Medical weight loss"), (None, "Brand-name options")], "Medical weight loss &middot; Telehealth") + f'''
<section><div class="wrap prose">
  {cta}
  <h2>How it works</h2>
  <div class="grid g3">
    <div class="card reveal"><span class="eyebrow">Step 1</span><h3>Video visit</h3><p>Complete the short <a href="{TELE["consent"]}" target="_blank" rel="noopener">telehealth consent</a>, then text, call or start a visit. Dr. Arora reviews your history, medications and goals by secure video.</p></div>
    <div class="card reveal"><span class="eyebrow">Step 2</span><h3>Prescription, if appropriate</h3><p>If a brand-name medication is a good fit, the prescription is sent to the manufacturer&rsquo;s self-pay pharmacy, or to your own pharmacy if you&rsquo;re using insurance.</p></div>
    <div class="card reveal"><span class="eyebrow">Step 3</span><h3>Delivered to your door</h3><p>You pay the pharmacy directly and the medication ships to your home. We follow up by video to adjust your dose and track progress.</p></div>
  </div>

  <h2>Manufacturer self-pay prices</h2>
  <p>Monthly cash prices set by the manufacturers for self-paying patients, as of {AS_OF}. Prices vary by dose.</p>
  <div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:.95rem" class="price-table">
    <thead><tr style="text-align:left;border-bottom:2px solid var(--line,#ddd)"><th style="padding:8px">Medication</th><th style="padding:8px">Dose</th><th style="padding:8px">Price</th><th style="padding:8px">Notes</th></tr></thead>
    <tbody>{rows}</tbody>
  </table></div>
  <style>.price-table td{{padding:8px;border-bottom:1px solid var(--line,#eee);vertical-align:top}}</style>
  <p style="font-size:.88rem;color:var(--muted)">Prices are set by the manufacturers, not by Serene, and may change or end at any time. Eligibility and restrictions apply. A lower price does not mean one medication works better or is safer than another. Serene&rsquo;s telehealth program is $149/month and is billed separately.</p>

  <h2>Is it right for me?</h2>
  <p>These medications are prescribed together with a reduced-calorie diet and more physical activity. They aren&rsquo;t right for everyone. They carry a boxed warning about thyroid C-cell tumors and should not be used by people with a personal or family history of medullary thyroid carcinoma or MEN 2. Common side effects include nausea, diarrhea, vomiting and constipation. Dr. Arora will review the full prescribing information, risks and alternatives with you before anything is prescribed.</p>
  <p>Prefer an in-office program? See our <a href="/weight-loss/">medical weight loss</a> options at our Hudson and Barboursville offices.</p>

  <h2>Questions</h2>
  <div class="grid g2">{faq_html}</div>
  {cta}
  <p style="background:#fff5f2;border-left:5px solid #c0392b;padding:14px 18px;border-radius:8px;font-weight:600;max-width:760px">Telehealth is not for emergencies. If you have a medical emergency, call 911.</p>
  <p style="font-size:.8rem;color:var(--muted)">Wegovy&reg; is a registered trademark of Novo Nordisk A/S. Zepbound&reg; and Foundayo&reg; are trademarks of their respective owners. Serene Med Spa is not affiliated with or endorsed by any manufacturer.</p>
</div></section>'''
    ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                     "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a.replace("&rsquo;", "'")}} for q, a in FAQ]}, ensure_ascii=False)
    return shell(SLUG, "Brand-Name Weight-Loss Medication Self-Pay Prices | Serene Telehealth",
                 "Self-pay prices for brand-name GLP-1 weight-loss medications, prescribed by telehealth with Robin Arora, MD in OH, WV, KY and FL. Delivered to your home.",
                 body, ld=ld)
