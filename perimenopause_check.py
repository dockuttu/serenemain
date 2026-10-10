# /perimenopause-check/ - 3-minute symptom check (Meta ad landing page, Oct 10 2026, approved by Robin).
# Runs entirely in the browser: answers are never stored or sent anywhere. No ad/analytics trackers on this page
# (Meta Pixel + Google tag are stripped in check_page()). Contact capture is a separate HIPAA Jotform (name/phone only).
# Public copy rules: no prescription drug names, no diagnosis, no guarantees, "physician-led team".
import re
from site_lib import shell, page_hero, book_band, HUDSON, BARB, TELE

CALLBACK = "https://form.jotform.com/262827129865065"
PATH = "/perimenopause-check/"

SYMPTOMS = [
    "Hot flashes or night sweats",
    "Trouble falling or staying asleep",
    "Heavier, longer or more irregular periods",
    "Mood swings, irritability or tearfulness",
    "Anxiety or feeling on edge",
    "Brain fog, forgetfulness or trouble concentrating",
    "Fatigue or low energy",
    "Joint or muscle aches",
    "Weight gain, especially around the middle",
    "Lower sex drive",
    "Vaginal dryness or discomfort with intimacy",
    "Breast tenderness, bloating or headaches before periods",
]

AGES = ["Under 35", "35&ndash;39", "40&ndash;44", "45&ndash;49", "50&ndash;55", "Over 55"]
CYCLES = [
    ("same", "About the same as always"),
    ("changed", "Changed: closer together, further apart, heavier or lighter"),
    ("skipped", "I&rsquo;ve skipped one or more months"),
    ("none12", "No period for 12 months or more"),
    ("na", "Not sure, or I don&rsquo;t have periods (for example after a hysterectomy or with an IUD)"),
]

CSS = """<style>
.pc{max-width:760px;margin:0 auto}
.pc-card{background:#fff;border:1px solid rgba(30,74,85,.14);border-radius:18px;padding:26px 24px;box-shadow:0 10px 30px rgba(27,42,47,.06)}
.pc-step{display:none}.pc-step.on{display:block}
.pc-prog{height:6px;background:var(--teal-100,#E3F0F2);border-radius:6px;margin:0 0 20px;overflow:hidden}
.pc-prog i{display:block;height:100%;width:0;background:var(--teal-500,#3E8FA0);transition:width .3s}
.pc h2{font-size:1.35rem;margin:0 0 6px}
.pc .pc-sub{color:var(--muted,#7C8A8F);font-size:.93rem;margin:0 0 18px}
.pc fieldset{border:0;margin:0 0 22px;padding:0}
.pc legend{font-weight:600;color:var(--ink,#1B2A2F);margin-bottom:10px;font-size:1rem}
.pc-opts{display:grid;gap:8px}
.pc-opts.two{grid-template-columns:repeat(auto-fill,minmax(150px,1fr))}
.pc-opt{display:flex;align-items:center;gap:10px;border:1px solid rgba(30,74,85,.2);border-radius:12px;padding:11px 14px;cursor:pointer;font-size:.95rem;line-height:1.35;background:#fff}
.pc-opt:has(input:checked){border-color:var(--teal-500,#3E8FA0);background:var(--teal-100,#E3F0F2)}
.pc-opt input{accent-color:var(--teal-700,#2A6F7F);flex:none;width:18px;height:18px;margin:0}
.pc-sym{border-top:1px solid rgba(30,74,85,.1);padding:14px 0}
.pc-sym:first-of-type{border-top:0}
.pc-sym p{margin:0 0 8px;font-weight:500;color:var(--ink,#1B2A2F)}
.pc-seg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.pc-seg label{text-align:center;border:1px solid rgba(30,74,85,.2);border-radius:10px;padding:9px 4px;cursor:pointer;font-size:.9rem;background:#fff}
.pc-seg label:has(input:checked){background:var(--teal-700,#2A6F7F);border-color:var(--teal-700,#2A6F7F);color:#fff}
.pc-seg input{position:absolute;opacity:0;pointer-events:none}
.pc-nav{display:flex;gap:10px;justify-content:space-between;align-items:center;margin-top:18px;flex-wrap:wrap}
.pc-err{color:#B4483F;font-size:.9rem;min-height:1.2em}
.pc-meter{display:flex;gap:4px;margin:14px 0 6px}.pc-meter span{flex:1;height:10px;border-radius:5px;background:var(--teal-100,#E3F0F2)}
.pc-meter span.f{background:var(--teal-500,#3E8FA0)}
.pc-band{font-size:1.25rem;font-weight:600;color:var(--teal-900,#1E4A55);margin:6px 0 10px}
.pc-note{background:var(--sand,#F4EEE6);border-radius:12px;padding:14px 16px;font-size:.93rem;margin:14px 0}
.pc-top{margin:10px 0 0;padding-left:20px}
.pc-cta{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 6px}
.pc-fine{font-size:.82rem;color:var(--muted,#7C8A8F);line-height:1.5;margin-top:16px}
.pc-lock{font-size:.85rem;color:var(--ink-soft,#4A5B61);display:flex;gap:8px;align-items:flex-start;margin:0 0 18px}
@media(max-width:520px){.pc-card{padding:20px 16px}.pc-seg label{font-size:.84rem}}
</style>"""


def _radio(name, value, label, req=False):
    return f'<label class="pc-opt"><input type="radio" name="{name}" value="{value}"{" required" if req else ""}><span>{label}</span></label>'


def check_page():
    ages = "".join(_radio("age", str(i), a) for i, a in enumerate(AGES))
    cycles = "".join(_radio("cycle", k, t) for k, t in CYCLES)
    syms = "".join(
        f'<div class="pc-sym" data-sym="{i}"><p>{s}</p><div class="pc-seg" role="radiogroup" aria-label="{s}">'
        + "".join(f'<label><input type="radio" name="s{i}" value="{v}"><span>{t}</span></label>' for v, t in ((0, "Never"), (1, "Sometimes"), (2, "Often")))
        + "</div></div>"
        for i, s in enumerate(SYMPTOMS))
    labels = "[" + ",".join('"' + s.replace('"', '') + '"' for s in SYMPTOMS) + "]"

    body = page_hero("Is it perimenopause&hellip; or just stress?",
                     "A 3-minute symptom check from the physician-led team at Serene Med Spa. Answer 14 quick questions and see how your symptoms line up with the common signs of perimenopause.",
                     [("/", "Home"), ("/perimenopause/", "Perimenopause"), (None, "Symptom check")], "3-minute symptom check") + f'''
<section><div class="wrap"><div class="pc">
 <p class="pc-lock"><span aria-hidden="true">&#128274;</span><span>Private by design: your answers stay on your device. Nothing is saved or sent, and this page has no ad tracking.</span></p>
 <div class="pc-card">
  <div class="pc-prog" aria-hidden="true"><i id="pc-bar"></i></div>
  <form id="pc-form" novalidate>
   <div class="pc-step on" data-step="1">
    <h2>About you</h2><p class="pc-sub">Step 1 of 2</p>
    <fieldset><legend>What is your age range?</legend><div class="pc-opts two">{ages}</div></fieldset>
    <fieldset><legend>How have your periods been over the last year?</legend><div class="pc-opts">{cycles}</div></fieldset>
    <fieldset><legend>Are you currently using hormonal birth control or hormone therapy?</legend><div class="pc-opts two">{_radio("horm","yes","Yes")}{_radio("horm","no","No")}{_radio("horm","unsure","Not sure")}</div></fieldset>
    <div class="pc-nav"><span class="pc-err" id="pc-err1" role="alert"></span><button type="button" class="btn" data-next>Next: symptoms &rarr;</button></div>
   </div>
   <div class="pc-step" data-step="2">
    <h2>Symptoms in the last 3 months</h2><p class="pc-sub">Step 2 of 2 &middot; How often have you noticed each one?</p>
    {syms}
    <div class="pc-nav"><button type="button" class="btn btn-outline" data-back>&larr; Back</button><span class="pc-err" id="pc-err2" role="alert"></span><button type="submit" class="btn">See my results</button></div>
   </div>
  </form>
  <div class="pc-step" id="pc-result" aria-live="polite" tabindex="-1">
   <h2>Your results</h2>
   <div class="pc-meter" id="pc-meter" aria-hidden="true"></div>
   <p class="pc-sub" id="pc-score"></p>
   <p class="pc-band" id="pc-band"></p>
   <p id="pc-msg"></p>
   <div id="pc-topwrap" hidden><strong>What you noticed most often:</strong><ul class="pc-top" id="pc-top"></ul></div>
   <div id="pc-extra"></div>
   <div class="pc-cta">
    <a class="btn" href="#book">Book a hormone consult</a>
    <a class="btn btn-outline" href="{CALLBACK}" target="_blank" rel="noopener">Have our team call me</a>
   </div>
   <p style="font-size:.93rem">Tip: jot down your top three symptoms and how long you&rsquo;ve had them, and bring the list to your visit. Want the background first? Read our <a href="/perimenopause/">perimenopause guide</a>.</p>
   <div class="pc-note"><strong>Please get checked soon</strong> if you have very heavy bleeding (soaking a pad or tampon every hour), bleeding between periods or after sex, or any bleeding after 12 months without a period. If you are having thoughts of harming yourself, call or text 988 any time.</div>
   <button type="button" class="btn btn-outline btn-sm" id="pc-again">Start over</button>
  </div>
  <p class="pc-fine">This check is for education only. It is not a diagnosis and doesn&rsquo;t replace a visit with a clinician. Many of these symptoms have other causes, such as thyroid problems, low iron, sleep disorders or stress, which is why an evaluation matters. Individual results vary.</p>
 </div>
</div></div></section>
{book_band()}
<script>
(function(){{
var L={labels};
var f=document.getElementById('pc-form'),bar=document.getElementById('pc-bar'),res=document.getElementById('pc-result');
function step(n){{[].forEach.call(f.querySelectorAll('.pc-step'),function(s){{s.classList.toggle('on',s.getAttribute('data-step')==n);}});bar.style.width=(n==1?'15%':'60%');f.scrollIntoView({{behavior:'smooth',block:'start'}});}}
function val(n){{var x=f.querySelector('input[name="'+n+'"]:checked');return x?x.value:null;}}
f.addEventListener('change',function(){{if(f.querySelector('[data-step="2"]').classList.contains('on')){{var a=0;for(var i=0;i<L.length;i++)if(val('s'+i)!==null)a++;bar.style.width=(60+40*a/L.length)+'%';}}}});
f.querySelector('[data-next]').addEventListener('click',function(){{var e=document.getElementById('pc-err1');if(!val('age')||!val('cycle')||!val('horm')){{e.textContent='Please answer all three questions.';return;}}e.textContent='';step(2);}});
f.querySelector('[data-back]').addEventListener('click',function(){{step(1);}});
f.addEventListener('submit',function(ev){{ev.preventDefault();var e=document.getElementById('pc-err2'),miss=[];for(var i=0;i<L.length;i++)if(val('s'+i)===null)miss.push(i);
 if(miss.length){{e.textContent='Please answer every symptom ('+miss.length+' left).';var m=f.querySelector('[data-sym="'+miss[0]+'"]');if(m)m.scrollIntoView({{behavior:'smooth',block:'center'}});return;}}e.textContent='';show();}});
function show(){{
 var s=0,often=[],some=[];for(var i=0;i<L.length;i++){{var v=+val('s'+i);s+=v;if(v==2)often.push(L[i]);else if(v==1)some.push(L[i]);}}
 var age=+val('age'),cyc=val('cycle'),horm=val('horm'),band,msg;
 if(s<=5){{band='Few symptoms right now';msg='You reported only a few of the symptoms that commonly come with perimenopause. If something still feels off, it&rsquo;s worth mentioning at your next checkup, and you can retake this check any time things change.';}}
 else if(s<=13){{band='Some symptoms worth talking about';msg='You reported several symptoms that often show up during perimenopause. A conversation with a clinician can help sort out what&rsquo;s hormonal, what isn&rsquo;t, and what might help.';}}
 else{{band='Many symptoms that often go with perimenopause';msg='You reported many of the symptoms commonly linked to perimenopause, and several of them often. You don&rsquo;t have to just push through it. A hormone consult with our physician-led team can look at the full picture, including labs to rule out other causes.';}}
 var ex=[];
 if((cyc==='changed'||cyc==='skipped')&&age>=2&&age<=4)ex.push('Changes in your cycle in your 40s or early 50s are one of the most common early signs of perimenopause.');
 if((cyc==='changed'||cyc==='skipped')&&age<=1)ex.push('Cycle changes before 40 can have many causes, including thyroid and other hormone conditions. They&rsquo;re worth an evaluation either way.');
 if(cyc==='none12')ex.push('Twelve months or more without a period usually means menopause rather than perimenopause. Many of the same symptoms continue, and care options are similar.');
 if(horm==='yes')ex.push('Hormonal birth control or hormone therapy can mask or change these symptoms, so bring that up at your visit.');
 var mt=document.getElementById('pc-meter');mt.innerHTML='';var lv=Math.round(s/24*10);for(var k=0;k<10;k++){{var sp=document.createElement('span');if(k<lv)sp.className='f';mt.appendChild(sp);}}
 document.getElementById('pc-score').textContent='Symptom score: '+s+' out of 24';
 document.getElementById('pc-band').textContent=band;document.getElementById('pc-msg').innerHTML=msg;
 var tw=document.getElementById('pc-topwrap'),tl=document.getElementById('pc-top');tl.innerHTML='';var top=often.length?often:some;
 top.slice(0,5).forEach(function(t){{var li=document.createElement('li');li.textContent=t;tl.appendChild(li);}});tw.hidden=!top.length;
 document.getElementById('pc-extra').innerHTML=ex.map(function(t){{return '<p class="pc-note" style="background:var(--teal-100,#E3F0F2)">'+t+'</p>';}}).join('');
 f.hidden=true;res.classList.add('on');bar.style.width='100%';res.focus({{preventScroll:true}});res.scrollIntoView({{behavior:'smooth',block:'start'}});
}}
document.getElementById('pc-again').addEventListener('click',function(){{f.reset();f.hidden=false;res.classList.remove('on');step(1);}});
bar.style.width='15%';
}})();
</script>'''
    html = shell(PATH, "Perimenopause Symptom Check (3 Minutes) | Serene Med Spa",
                 "Is it perimenopause or just stress? Take a free, private 3-minute symptom check from the physician-led team at Serene Med Spa. Answers stay on your device.",
                 body, extra_head=CSS)
    # No trackers on this page: strip the Meta Pixel and the Google tag blocks from the shared shell.
    html = re.sub(r'<!-- Meta Pixel -->.*?</noscript>', '', html, flags=re.S)
    html = re.sub(r'<!-- Google Ads tag -->\s*<script async src="https://www\.googletagmanager\.com/gtag/js[^"]*"></script>\s*<script>.*?</script>', '', html, flags=re.S)
    return html
