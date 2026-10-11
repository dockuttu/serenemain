#!/usr/bin/env python3
# add_text_links.py — put a "Text" option right before every "Call" option (Robin, Oct 10 2026: "Add text option before
# the call option but keep both options"). Text numbers are the Mangomint two-way texting numbers for each office.
# Runs LAST on a built site folder (after every injector / shell merge). Idempotent: links it adds carry data-txt.
# Same file in serenemain, serenehudson and serenebarboursville.
#   usage: python3 add_text_links.py bundle/site
import os, re, sys

TEXT = {  # office call number -> (Mangomint texting number, display)
    "+13304605915": ("+13303032031", "(330) 303-2031"),   # Hudson
    "+13045200461": ("+13043960295", "(304) 396-0295"),   # Barboursville
}
MBAR_CSS = '<style id="txt-css">.mbar a{padding:14px 6px!important;letter-spacing:.08em!important}</style>'
A_RE = re.compile(r'<a\b([^>]*?)href="tel:(\+1\d{10})"([^>]*)>(.*?)</a>', re.S)

def _cls(attrs):
    m = re.search(r'class="([^"]*)"', attrs)
    return m.group(1) if m else ""

def process(html):
    out, pos, changed = [], 0, False
    for m in A_RE.finditer(html):
        num = m.group(2)
        if num not in TEXT:
            continue
        sms, disp = TEXT[num]
        attrs = m.group(1) + m.group(3)
        before = html[max(0, m.start() - 400):m.start()]
        if 'data-txt' in before[-260:] and ('sms:' + sms) in before[-260:]:
            continue                                   # already has its Text option
        cls = _cls(attrs)
        start, ins, call_html = m.start(), None, m.group(0)
        if "mbar-call" in cls:
            ins = f'<a class="{cls}" data-txt href="sms:{sms}">&#9993;&nbsp; Text</a>'
        elif re.search(r'\bbtn\b', cls):
            ins = f'<a class="{cls}" data-txt href="sms:{sms}">Text {disp}</a> '
        elif re.search(r'<li[^>]*>\s*$', before):
            li = re.search(r'<li[^>]*>\s*$', before)
            start = m.start() - (len(before) - li.start())
            ins = f'<li><a data-txt href="sms:{sms}">Text us: {disp}</a></li>'
            inner = m.group(4)
            if inner.lstrip().startswith("("):
                call_html = call_html.replace(">" + inner + "</a>", ">Call: " + inner + "</a>", 1)
            call_html = before[li.start():] + call_html
        elif re.search(r'<div class="row"><strong>Call</strong><span>\s*$', before):
            r = re.search(r'<div class="row"><strong>Call</strong><span>\s*$', before)
            start = m.start() - (len(before) - r.start())
            ins = f'<div class="row"><strong>Text</strong><span><a data-txt href="sms:{sms}">{disp}</a></span></div>'
            call_html = before[r.start():] + call_html
        elif re.search(r'\b([Cc]all)\s+$', before):
            w = re.search(r'\b([Cc]all)\s+$', before)
            start = m.start() - (len(before) - w.start())
            word = "Text" if w.group(1) == "Call" else "text"
            ins = f'{word} <a data-txt href="sms:{sms}">{disp}</a> or call '
            call_html = call_html
        if ins is None:
            continue
        out.append(html[pos:start]); out.append(ins + call_html); pos = m.end(); changed = True
    if not changed:
        return html, False
    out.append(html[pos:])
    html = "".join(out)
    if 'class="mbar' in html and 'id="txt-css"' not in html and "</head>" in html:
        html = html.replace("</head>", MBAR_CSS + "</head>", 1)
    return html, True

def main(root):
    n = 0
    for dp, _, fs in os.walk(root):
        for f in fs:
            if not f.endswith(".html") or f.startswith("._"):
                continue
            p = os.path.join(dp, f)
            try:
                s = open(p, encoding="utf-8").read()
            except Exception:
                continue
            t, ch = process(s)
            if ch:
                open(p, "w", encoding="utf-8").write(t); n += 1
    print(f"add_text_links: Text option added on {n} pages")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "bundle/site")
