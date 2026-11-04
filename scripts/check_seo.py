#!/usr/bin/env python3
"""SEO structure check (read-only, offline). Fails (exit 1) if:
- a row in data/old-article-redirects.csv points to a missing /articles/ file,
  or its redirect stub is missing / points somewhere else / lacks noindex;
- sitemap.xml lists a URL with no matching file, or misses a live page or article;
- an /articles/ page lacks a self-referencing canonical;
- two indexable pages share a <title> or an <h1>.
Run: python3 scripts/check_seo.py"""
import csv, os, re, sys, html
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://hinderliterhearing.com"
err = []
def rd(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()

rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "old-article-redirects.csv"))))
for r in rows:
    tgt = r["new_path"]
    if not os.path.isfile(os.path.join(ROOT, tgt.lstrip("/"))): err.append(f"missing target {tgt}")
    sp = r["old_path"].strip("/") + "/index.html"
    if not os.path.isfile(os.path.join(ROOT, sp)): err.append(f"missing stub {sp}"); continue
    s = rd(sp); url = BASE + tgt
    for need in (f'<link rel="canonical" href="{url}">', f'content="0; url={url}"',
                 f'location.replace("{url}")', 'content="noindex, follow"'):
        if need not in s: err.append(f"{sp}: missing {need}")

arts = sorted(f for f in os.listdir(os.path.join(ROOT, "articles")) if f.endswith(".html"))
for f in arts:
    if f'<link rel="canonical" href="{BASE}/articles/{f}">' not in rd("articles/" + f):
        err.append(f"articles/{f}: no self canonical")

locs = re.findall(r"<loc>(.*?)</loc>", rd("sitemap.xml"))
if len(locs) != len(set(locs)): err.append("sitemap has duplicate <loc>")
want = {BASE + "/"} | {f"{BASE}/{f}" for f in os.listdir(ROOT) if f.endswith(".html") and f not in ("index.html", "404.html")} \
       | {f"{BASE}/articles/{f}" for f in arts}
for l in set(locs) - want: err.append(f"sitemap lists unknown URL {l}")
for l in want - set(locs): err.append(f"sitemap missing {l}")

pages = [f for f in os.listdir(ROOT) if f.endswith(".html") and f != "404.html"] + ["articles/" + f for f in arts]
seen_t, seen_h = {}, {}
for p in pages:
    s = rd(p)
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    h = re.findall(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not t: err.append(f"{p}: no <title>"); continue
    if len(h) != 1: err.append(f"{p}: {len(h)} <h1>"); continue
    t = html.unescape(t.group(1)).strip()
    h = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h[0]))).strip()
    if t in seen_t: err.append(f"duplicate title '{t}': {seen_t[t]} and {p}")
    if h in seen_h: err.append(f"duplicate h1 '{h}': {seen_h[h]} and {p}")
    seen_t[t] = p; seen_h[h] = p

if err:
    print("SEO CHECK FAILED"); print("\n".join(err)); sys.exit(1)
print(f"SEO check passed: {len(rows)} redirect stubs -> existing articles; {len(locs)} sitemap URLs "
      f"({len(want) - len(arts)} pages + {len(arts)} articles); {len(arts)} article canonicals; "
      f"{len(pages)} unique titles and H1s.")
