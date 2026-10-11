# /refer-a-friend/ - client referral program, all offices (Robin, Oct 11 2026: "I always had a referral in Barboursville. lets do it";
# terms chosen: "$50 credit for you both", same as Paintsville). Not tied to reviews or social posts.
from site_lib import shell, page_hero, HUDSON, BARB

def refer_page():
    body = page_hero("Refer a friend: $50 for you both", "Love your results? Send a friend to Serene. They get $50 off their first visit, and you get a $50 credit once their visit is complete.",
                     [("/", "Home"), (None, "Refer a friend")], "Referral program") + f'''
<section><div class="wrap" style="display:grid;grid-template-columns:minmax(0,6fr) minmax(0,5fr);gap:36px;align-items:start">
  <div class="prose">
    <h2>How it works</h2>
    <ol>
      <li><strong>Tell a friend about Serene.</strong> Share this page or just give them your name.</li>
      <li><strong>Your friend books their first visit</strong> and enters your name under &ldquo;Referral&rdquo; on our new-client form (or tells the front desk).</li>
      <li><strong>Your friend saves $50</strong> on that first visit.</li>
      <li><strong>You get a $50 credit</strong> on your Serene account after their visit is paid. Use it on any treatment or product.</li>
    </ol>
    <p>There&rsquo;s no limit on how many friends you can refer. Questions? Text Hudson at <a data-txt href="sms:{HUDSON["sms"]}">{HUDSON["text"]}</a> or Barboursville at <a data-txt href="sms:{BARB["sms"]}">{BARB["text"]}</a>.</p>
    <p style="font-size:.85rem;color:var(--muted)"><strong>Program terms:</strong> For referrals of new clients age 18 or older who have never visited a Serene Med Spa office. Your friend&rsquo;s $50 off applies to their first paid visit of $100 or more and can&rsquo;t be combined with the 20% new-client offer or any other discount. Your $50 credit is added to your client account after your friend&rsquo;s first visit is paid; it has no cash value, can&rsquo;t be transferred and expires 12 months after it&rsquo;s issued. Treatment is provided only if it&rsquo;s right for your friend after their consultation. Rewards are never tied to reviews or social media posts. Serene Med Spa may change or end the program at any time; credits already earned will be honored.</p>
  </div>
  <div class="card" style="padding:28px">
    <h3 style="margin-top:0">Ready to send a friend?</h3>
    <p>Share this link:</p>
    <p style="font-weight:600;word-break:break-all">serenemedspas.com/refer-a-friend/</p>
    <p style="margin-bottom:8px">Your friend can book online:</p>
    <p><a class="btn" href="{HUDSON["book"]}" target="_blank" rel="noopener">Book Hudson</a> <a class="btn" href="{BARB["book"]}" target="_blank" rel="noopener">Book Barboursville</a></p>
  </div>
</div></section>
<style>@media(max-width:860px){{section .wrap[style*="grid-template-columns"]{{grid-template-columns:1fr!important}}}}</style>'''
    return shell("/refer-a-friend/", "Refer a Friend: $50 for You Both | Serene Med Spa",
                 "Refer a friend to Serene Med Spa in Hudson, OH or Barboursville, WV: they get $50 off their first visit and you get a $50 account credit.",
                 body)
