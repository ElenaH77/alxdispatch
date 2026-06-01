#!/usr/bin/env python3
"""alxdispatch.org static site generator.

Stitches the per-page content fragments in src/ into full pages using the
shared skeleton (partials/base.html) + a single shared nav and footer, so the
five-item header and footer are defined once and stay consistent everywhere.

Run from anywhere:  python3 build.py
Output: index.html and <page>/index.html written into this repo root, plus a
shared nav bar injected into the copied May archive page (archive/2026-05/).

Adding a month later: copy the month's published page into archive/<YYYY-MM>/,
add it to ARCHIVE_MONTHS below and to src/archive.html, append its rows to
incidents.csv (card_url -> /archive/<YYYY-MM>/#incident-NN), then re-run.
"""
import os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://alxdispatch.org"

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("  wrote", rel)

BASE   = read("partials/base.html")
FOOTER = read("partials/footer.html")

# Primary nav: five items max, evergreen-first, archive demoted to a dropdown.
# (Data lives in the footer + inline links, per the IA spec.)
APRIL_URL = "https://elenah77.github.io/what-dispatch-heard-in-april/"

def header(active):
    def link(key, href, label):
        cls = ' class="active"' if active == key else ""
        return f'<a href="{href}"{cls}>{label}</a>'
    archive_active = ' class="active"' if active == "archive" else ""
    return f"""<header class="site">
  <a class="wordmark" href="/">ALX Dispatch<span class="dot">.</span></a>
  <nav class="site">
    {link("map", "/", "Map")}
    {link("methodology", "/methodology/", "Methodology")}
    {link("recommendations", "/recommendations/", "Recommendations")}
    <span class="drop"><a href="/archive/"{archive_active}>Archive</a>
      <span class="menu">
        <a href="/archive/2026-05/">May 2026<small>What dispatch heard in May</small></a>
        <a href="{APRIL_URL}" target="_blank" rel="noopener">April 2026<small>The original retrospective &#8599;</small></a>
        <a href="/archive/">All months</a>
      </span>
    </span>
    {link("about", "/about/", "About")}
  </nav>
</header>"""

def page(content, title, description, canonical, active, extra_head=""):
    out = BASE
    repl = {
        "{{title}}": html.escape(title, quote=True),
        "{{description}}": html.escape(description, quote=True),
        "{{canonical}}": canonical,
        "{{extra_head}}": extra_head,
        "{{header}}": header(active),
        "{{content}}": content,
        "{{footer}}": FOOTER,
    }
    for k, v in repl.items():
        out = out.replace(k, v)
    return out

# (src fragment, output path, title, description, canonical, nav-active key)
PAGES = [
    ("src/home.html", "index.html",
     "What Dispatch Heard — Alexandria, VA",
     "A cumulative map of pedestrian, cyclist, and scooter strikes — plus crashes on Braddock Road and Mount Vernon Avenue — captured from Alexandria's public dispatch audio. Updated monthly.",
     SITE + "/", "map"),
    ("src/methodology.html", "methodology/index.html",
     "Methodology — ALX Dispatch",
     "How this data is gathered: public dispatch audio from OpenMHz, Whisper transcription, an automated flagging pipeline, and human review — and why dispatch sees strikes the official crash record misses.",
     SITE + "/methodology/", "methodology"),
    ("src/recommendations.html", "recommendations/index.html",
     "Recommendations — ALX Dispatch",
     "What Alexandria should do: a Charlottesville-style reporting general order, monthly dispatch-audio screening, and an expanded DASH–NVFSS near-miss reporting partnership.",
     SITE + "/recommendations/", "recommendations"),
    ("src/data.html", "data/index.html",
     "The data — ALX Dispatch",
     "Download the dataset behind the map: incidents.csv, a full column dictionary, reuse terms, and the scope and accuracy caveats.",
     SITE + "/data/", "data"),
    ("src/about.html", "about/index.html",
     "About — ALX Dispatch",
     "A personal civic-data project mapping Alexandria pedestrian, cyclist, and scooter strikes from public dispatch audio, with a plan to hand monthly screening to NVFSS.",
     SITE + "/about/", "about"),
    ("src/archive.html", "archive/index.html",
     "Archive — ALX Dispatch",
     "The monthly write-ups behind the map, newest first: the narrative for each month with the original dispatch audio.",
     SITE + "/archive/", "archive"),
]

# Months that have been copied in as in-site archive pages. Each gets the shared
# nav bar injected so visitors aren't stranded inside a standalone month page.
ARCHIVE_MONTHS = ["archive/2026-05"]

NAVBAR_MARK = "<!--alx-navbar-->"
def navbar_html():
    return f"""{NAVBAR_MARK}
<div style="background:#234969;color:#fff;font-family:'Work Sans',-apple-system,Segoe UI,Roboto,sans-serif;display:flex;flex-wrap:wrap;align-items:center;gap:6px 18px;padding:11px 18px;font-size:13.5px;">
  <a href="/" style="color:#fff;text-decoration:none;font-weight:600;margin-right:auto;">ALX Dispatch<span style="color:#F2CC44;">.</span></a>
  <span style="display:flex;flex-wrap:wrap;gap:4px 14px;">
    <a href="/" style="color:#fff;text-decoration:none;">Map</a>
    <a href="/methodology/" style="color:#fff;text-decoration:none;">Methodology</a>
    <a href="/recommendations/" style="color:#fff;text-decoration:none;">Recommendations</a>
    <a href="/archive/" style="color:#fff;text-decoration:none;">Archive</a>
    <a href="/about/" style="color:#fff;text-decoration:none;">About</a>
  </span>
</div>"""

def inject_navbar(month_dir):
    idx = os.path.join(ROOT, month_dir, "index.html")
    if not os.path.exists(idx):
        print("  SKIP nav inject (missing):", month_dir, "/index.html")
        return
    with open(idx, encoding="utf-8") as f:
        doc = f.read()
    if NAVBAR_MARK in doc:  # idempotent: strip the previously-injected bar first
        doc = re.sub(re.escape(NAVBAR_MARK) + r".*?</div>\s*", "", doc, count=1, flags=re.S)
    bar = navbar_html()
    doc = re.sub(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + bar, doc, count=1)
    with open(idx, "w", encoding="utf-8") as f:
        f.write(doc)
    print("  injected nav bar ->", month_dir + "/index.html")

def main():
    print("Building alxdispatch.org ...")
    for src, out, title, desc, canon, active in PAGES:
        page_html = page(read(src), title, desc, canon, active)
        write(out, page_html)
    for m in ARCHIVE_MONTHS:
        inject_navbar(m)
    print("Done.")

if __name__ == "__main__":
    main()
