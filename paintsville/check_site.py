#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_site.py — QA for the built site (run automatically at the end of gen_site.py; non-fatal there).

Asserts, for every built HTML page: exactly one <h1>, <title> <= 60 chars, meta description 120-155 chars,
canonical present, every JSON-LD block parses, no forbidden phrases, no broken internal links or missing images
(including srcset variants), alt text on every <img>.
"""
import os, re, sys, json, html
from html.parser import HTMLParser

FORBIDDEN = [r"vaginal rejuvenation", r"permanent hair", r"permanent(ly)? (removal|reduction)", r"laser lipo", r"lipo\b",
             r"semaglutide", r"tirzepatide", r"ozempic", r"wegovy", r"mounjaro", r"zepbound", r"belmar", r"compounding pharmacy", r"phentermine"]

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.h1 = 0; self.title = ""; self.desc = None; self.canon = None; self.links = []; self.imgs = []; self.ld = []; self._in = None; self._ld = False; self.alts_missing = 0; self.iframes = []
    def handle_starttag(self, t, a):
        a = dict(a)
        if t == "h1": self.h1 += 1
        elif t == "title": self._in = "title"
        elif t == "meta" and a.get("name") == "description": self.desc = a.get("content", "")
        elif t == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        elif t == "a" and a.get("href"): self.links.append(a["href"])
        elif t == "img":
            self.imgs.append(a.get("src", ""))
            for part in (a.get("srcset") or "").split(","):
                u = part.strip().split(" ")[0]
                if u: self.imgs.append(u)
            if not a.get("alt", None) and a.get("alt") != "": self.alts_missing += 1
            if "alt" not in a: self.alts_missing += 1
        elif t == "script" and a.get("type") == "application/ld+json": self._ld = True; self._buf = ""
        elif t == "iframe": self.iframes.append(a.get("src", ""))
    def handle_endtag(self, t):
        if t == "title": self._in = None
        if t == "script" and self._ld: self.ld.append(self._buf); self._ld = False
    def handle_data(self, d):
        if self._in == "title": self.title += d
        if self._ld: self._buf += d

def run(out):
    errs, warns, n = [], [], 0
    pages = []
    for root, _, files in os.walk(out):
        for f in files:
            if f.endswith(".html") and not f.startswith("google"): pages.append(os.path.join(root, f))  # skip Search Console verification file
    for fp in sorted(pages):
        n += 1
        rel = "/" + os.path.relpath(fp, out).replace(os.sep, "/")
        raw = open(fp, encoding="utf-8").read()
        p = P(); p.feed(raw)
        text = html.unescape(re.sub(r"<[^>]+>", " ", raw)).lower()
        if p.h1 != 1: errs.append(f"{rel}: {p.h1} <h1> tags")
        t = html.unescape(p.title.strip())
        if not (10 <= len(t) <= 60): errs.append(f"{rel}: title length {len(t)}: {t!r}")
        d = html.unescape(p.desc or "")
        if not (120 <= len(d) <= 155): errs.append(f"{rel}: description length {len(d)}: {d!r}")
        if not p.canon: errs.append(f"{rel}: no canonical")
        if not p.ld and "404" not in rel: errs.append(f"{rel}: no JSON-LD")
        for b in p.ld:
            try: json.loads(b)
            except Exception as e: errs.append(f"{rel}: JSON-LD parse error: {e}")
        for pat in FORBIDDEN:
            m = re.search(pat, text)
            if m: errs.append(f"{rel}: forbidden phrase {m.group(0)!r}")
        if p.alts_missing: errs.append(f"{rel}: {p.alts_missing} <img> without alt")
        for href in p.links:
            h = href.split("#")[0]
            if not h or not h.startswith("/") : continue
            target = os.path.join(out, h.lstrip("/"), "index.html") if h.endswith("/") else os.path.join(out, h.lstrip("/"))
            if not os.path.exists(target): errs.append(f"{rel}: broken link {href}")
        for src in p.imgs:
            if src.startswith("/") and not os.path.exists(os.path.join(out, src.lstrip("/"))): errs.append(f"{rel}: missing image {src}")
        if "TODO" in raw: warns.append(f"{rel}: contains literal 'TODO' (unfilled constant?)")
    for req in ("sitemap.xml", "robots.txt", "favicon.svg", "site.webmanifest", "main.css", "404.html"):
        if not os.path.exists(os.path.join(out, req)): errs.append(f"missing {req}")
    out_s = sys.stderr if errs else sys.stdout
    print(f"\nQA: {n} pages checked — {len(errs)} error(s), {len(warns)} warning(s)", file=out_s)
    for w in warns: print("  WARN", w, file=sys.stderr)
    for e in errs: print("  ERROR", e, file=sys.stderr)
    return 1 if errs else 0

if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bundle", "paintsville", "site"))))
