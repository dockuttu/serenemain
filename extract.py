# -*- coding: utf-8 -*-
"""extract.py — pull title/meta/content out of the WordPress (Elementor/Astra) snapshot pages in mirror/."""
import re, os, html, json

VOID = {"img", "br", "hr", "source", "input", "meta", "link"}
KEEP_ATTRS = {"a": ("href", "target", "rel", "title"), "img": ("src", "srcset", "sizes", "alt", "width", "height", "loading"),
              "source": ("srcset", "type", "media"), "td": ("colspan", "rowspan"), "th": ("colspan", "rowspan"), "iframe": ("src", "title", "allow", "allowfullscreen", "loading", "width", "height")}
KEEP_TAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "strong", "b", "em", "i", "a", "img", "br", "blockquote", "table", "thead", "tbody", "tr", "td", "th",
             "figure", "figcaption", "picture", "source", "iframe", "sup", "sub", "u", "s", "hr", "dl", "dt", "dd", "code", "pre", "span", "div", "section", "details", "summary", "video", "audio"}

def meta(s):
    def g(rx, default=""):
        m = re.search(rx, s, re.I | re.S); return html.unescape(m.group(1)).strip() if m else default
    title = g(r"<title>([^<]*)</title>")
    title = re.sub(r"\s*[\-|–]\s*Serene Med Spas?\s*$", "", title).strip() or title
    return {
        "title": title,
        "description": g(r'<meta name="description" content="([^"]*)"'),
        "og_image": g(r'<meta property="og:image" content="([^"]*)"'),
        "published": g(r'<meta property="article:published_time" content="([^"]*)"') or g(r'"datePublished":"([^"]*)"'),
        "modified": g(r'<meta property="article:modified_time" content="([^"]*)"') or g(r'"dateModified":"([^"]*)"'),
        "author": g(r'"author":\{"@type":"Person","name":"([^"]*)"') or g(r'<meta name="author" content="([^"]*)"'),
        "h1": g(r"<h1[^>]*>(.*?)</h1>"),
    }

def balanced(s, start_rx):
    """Return the inner HTML of the first <div ...> matching start_rx (balanced on <div>/</div>)."""
    m = re.search(start_rx, s)
    if not m: return ""
    i = m.end(); depth = 1
    for t in re.finditer(r"<div\b|</div>", s[i:]):
        depth += 1 if t.group(0) == "<div" else -1
        if depth == 0: return s[i:i + t.start()]
    return s[i:]

def page_container(s):
    """Content container: nested wp-post inside theme-post-content (posts) or the wp-page container (pages)."""
    inner = balanced(s, r'<div[^>]*elementor-widget-theme-post-content[^>]*>')
    if inner:
        c = balanced(inner, r'<div data-elementor-type="wp-post"[^>]*>') or balanced(inner, r'<div class="elementor-widget-container">')
        if c: return c
    c = balanced(s, r'<div data-elementor-type="wp-page"[^>]*>')
    if c: return c
    return balanced(s, r'<div class="entry-content[^"]*"[^>]*>')

def html_widgets(container):
    """Raw inner HTML of every Elementor HTML widget (self-styled blocks pasted into the page)."""
    out = []
    for m in re.finditer(r'<div[^>]*elementor-widget-html[^>]*>', container):
        w = balanced(container[m.start():], r'<div[^>]*elementor-widget-html[^>]*>')
        inner = balanced(w, r'<div class="elementor-widget-container">') or w
        out.append(inner)
    return out

def widget_body(raw):
    """A pasted full HTML document -> just its <body> inner (keeping its <style>); otherwise as-is."""
    m = re.search(r"<body[^>]*>(.*)</body>", raw, re.S | re.I)
    body = m.group(1) if m else raw
    # pull <style> blocks from a pasted <head> so scoped styles survive
    head = re.search(r"<head[^>]*>(.*?)</head>", raw, re.S | re.I)
    styles = "".join(re.findall(r"<style[^>]*>.*?</style>", head.group(1), re.S | re.I)) if head else ""
    body = re.sub(r"<!DOCTYPE[^>]*>", "", body, flags=re.I)
    return styles + body

def simplify(h):
    """Reduce Elementor markup to clean semantic HTML: drop wrappers, classes, emoji images, scripts."""
    h = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", "", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    h = re.sub(r'<img[^>]*fonts\.gstatic\.com/s/e/notoemoji[^>]*>', "", h)   # emoji as images
    h = re.sub(r'<(?:svg)\b.*?</svg>', "", h, flags=re.S | re.I)
    h = re.sub(r'<(?:button)\b[^>]*>.*?</button>', "", h, flags=re.S | re.I)
    # Elementor accordion / toggle -> details
    h = re.sub(r'<div class="elementor-tab-title"[^>]*>(.*?)</div>', lambda m: "<summary>" + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "</summary>", h, flags=re.S)
    h = re.sub(r'<div class="elementor-tab-content[^"]*"[^>]*>', "<div>", h)
    def tag(m):
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3) or ""
        if name not in KEEP_TAGS: return ""
        if name in ("div", "section", "span"):
            # keep only structural div for accordion items; everything else vanishes
            if name == "div" and "elementor-accordion-item" in attrs: return "</details>" if close else "<details>"
            return ""
        if close: return f"</{name}>"
        keep = KEEP_ATTRS.get(name, ())
        out = []
        for k in keep:
            am = re.search(r'\b' + k + r'="([^"]*)"', attrs)
            if am: out.append(f'{k}="{am.group(1)}"')
        if name == "a" and any(x.startswith("href=") for x in out) and 'href="#' in "".join(out): return ""  # in-page anchors from accordions
        return f"<{name}{(' ' + ' '.join(out)) if out else ''}>"
    h = re.sub(r"<(/?)([a-zA-Z0-9]+)((?:\s+[^>]*?)?)\s*/?>", tag, h)
    # tidy
    h = re.sub(r"<p>\s*(?:&nbsp;|\s)*</p>", "", h)
    h = re.sub(r"<(strong|em|b|i|span)>\s*</\1>", "", h)
    h = re.sub(r"\n\s*\n+", "\n", h)
    h = re.sub(r"<a>(.*?)</a>", r"\1", h, flags=re.S)   # anchors with no href kept
    h = re.sub(r"<(h[1-6])>\s*</\1>", "", h)
    h = re.sub(r"<li>\s*</li>", "", h)
    h = re.sub(r"</details>\s*<details>", "</details>\n<details>", h)
    return h.strip()

def text_of(h, n=None):
    t = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)[^>]*>.*?</\1>", "", h, flags=re.S)))
    t = re.sub(r"\s+", " ", t).strip()
    return t[:n] if n else t

def load(mirror, slug):
    p = os.path.join(mirror, slug.strip("/"), "index.html") if slug.strip("/") else os.path.join(mirror, "index.html")
    if not os.path.exists(p): return None
    s = open(p, encoding="utf-8", errors="replace").read()
    m = meta(s); m["slug"] = "/" + slug.strip("/") + "/" if slug.strip("/") else "/"
    m["raw"] = s
    m["container"] = page_container(s)
    return m
