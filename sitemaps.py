#!/usr/bin/env python3
"""
sitemaps.py - writes the two maps search engines use to find our pages.

WHAT THIS DOES, PLAIN ENGLISH
-----------------------------
  docs/sitemap.xml       every public page on the site, so Google and Bing
                         know it exists. Rebuilt from what is really in docs/.
  docs/news-sitemap.xml  only our own news stories from the last 48 hours,
                         which is the window Google News asks for. Press
                         releases are left out: this file is for reporting.

Held stories never appear in either file. A story is held when it has no
signed_off_by, or when its embargo time has not arrived (same rule as
wire.py, imported from it so the two can never disagree).

  python3 sitemaps.py             write both files
  python3 sitemaps.py --indexnow  write both, then tell IndexNow (Bing,
                                  Yandex, Naver, Seznam) about fresh URLs

The IndexNow key file docs/56bacd32bafcff9940a1156e40beb164.txt proves we own the
domain. Deleting it silently breaks submission. Cost: zero.
"""

import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

import wire

INDEXNOW_KEY = "56bacd32bafcff9940a1156e40beb164"
HOST = "worldnewswirepress.com"
NEWS_WINDOW_HOURS = 48


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def git_lastmod(path):
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", path],
                             capture_output=True, text=True, timeout=30, cwd=wire.ROOT).stdout.strip()
        return out or None
    except Exception:
        return None


def main():
    now = datetime.now(timezone.utc)
    live, held = wire.load_originated(now)
    held_urls = {a["url"] for a, _ in held}
    live_by_url = {a["url"]: a for a in live}

    # ---- full sitemap: every real page on disk, minus held ones -----------
    pages = []
    for name in sorted(os.listdir(wire.DOCS)):
        if not name.endswith(".html") or name.startswith("_") or name in held_urls:
            continue
        text = open(os.path.join(wire.DOCS, name), encoding="utf-8", errors="replace").read()
        if re.search(r'http-equiv=["\']?refresh', text, re.I):
            continue                                   # redirect stub, not a page
        if name == "index.html":
            loc, freq, pri = wire.SITE + "/", "hourly", "1.0"
        elif name in wire.GENERATED:
            loc, freq, pri = wire.SITE + "/" + name, "hourly", "0.9"
        else:
            loc, freq, pri = wire.SITE + "/" + name, "weekly", "0.8"
        a = live_by_url.get(name)
        mod = git_lastmod(os.path.join("docs", name)) or (a and a["date"]) or now.strftime("%Y-%m-%d")
        pages.append((loc, mod, freq, pri))
    pages.sort(key=lambda p: (p[0] != wire.SITE + "/", p[0]))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, mod, freq, pri in pages:
        lines.append("  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq>"
                     "<priority>%s</priority></url>" % (loc, mod, freq, pri))
    lines.append("</urlset>\n")
    open(os.path.join(wire.DOCS, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines))

    # ---- news sitemap: our live stories from the last 48 hours ------------
    cutoff = now - timedelta(hours=NEWS_WINDOW_HOURS)
    news = []
    for a in live:
        if a.get("kind") == "release" or a.get("sponsored"):
            continue
        pub = wire.parse_when(a.get("published") or a["date"])
        if pub < cutoff or not os.path.exists(os.path.join(wire.DOCS, a["url"])):
            continue
        news.append((a, pub))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
             '        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">']
    for a, pub in news:
        lines += ["  <url>", "    <loc>%s/%s</loc>" % (wire.SITE, a["url"]), "    <news:news>",
                  "      <news:publication><news:name>%s</news:name><news:language>en</news:language></news:publication>" % wire.NAME,
                  "      <news:publication_date>%s</news:publication_date>" % pub.isoformat(),
                  "      <news:title>%s</news:title>" % esc(a["title"]), "    </news:news>", "  </url>"]
    lines.append("</urlset>\n")
    open(os.path.join(wire.DOCS, "news-sitemap.xml"), "w", encoding="utf-8").write("\n".join(lines))
    print("sitemap.xml: %d pages | news-sitemap.xml: %d stories | held: %d"
          % (len(pages), len(news), len(held)))

    if "--indexnow" in sys.argv:
        urls = ["%s/%s" % (wire.SITE, a["url"]) for a, _ in news]
        # On a push, also announce releases and pages, which the news map leaves out.
        if os.environ.get("GITHUB_EVENT_NAME") == "push":
            urls += [p[0] for p in pages if p[0] not in urls][:200]
        if not urls:
            print("IndexNow: nothing fresh to submit")
            return
        body = json.dumps({"host": HOST, "key": INDEXNOW_KEY,
                           "keyLocation": "https://%s/%s.txt" % (HOST, INDEXNOW_KEY),
                           "urlList": urls}).encode()
        req = urllib.request.Request("https://api.indexnow.org/IndexNow", data=body, method="POST",
                                     headers={"Content-Type": "application/json; charset=utf-8"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                print("IndexNow accepted %d URLs (HTTP %d)" % (len(urls), r.status))
        except Exception as exc:
            # Never fail the run over this: the sitemaps are the source of truth.
            print("IndexNow submission failed, sitemaps still written: %s" % exc)


if __name__ == "__main__":
    main()
