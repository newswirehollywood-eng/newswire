#!/usr/bin/env python3
"""CONTACT CHECKER. Plain English: opens each outlet's public contact page in a
real browser and records every email address printed on it, so our news-desk
list only uses addresses the outlet itself publishes. Writes
<csv>-verified.csv next to the input. Usage: verify_contacts.py <csv>"""
import csv, re, sys
from datetime import datetime, timezone
from playwright.sync_api import sync_playwright
src = sys.argv[1]
rows = list(csv.DictReader(open(src, encoding="utf-8")))
EM = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
BAD = re.compile(r"\.(png|jpe?g|gif|webp|svg)$|sentry|wixpress|example\.|@\dx", re.I)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_context(user_agent="Mozilla/5.0 (Macintosh) NewswireHollywoodContactCheck/1.0").new_page()
    for r in rows:
        r["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        try:
            resp = pg.goto(r["source_url"], wait_until="domcontentloaded", timeout=40000)
            pg.wait_for_timeout(2500)
            html = pg.content()
            found = sorted({e for e in EM.findall(html) if not BAD.search(e)}, key=str.lower)
            r["http_status"] = resp.status if resp else ""
            r["emails_on_page"] = " ".join(found)
            r["listed_email_on_page"] = ("yes" if r["email"] and r["email"].lower() in html.lower() else ("no" if r["email"] else ""))
        except Exception as e:
            r["http_status"] = "error: %s" % str(e)[:80]
            r["emails_on_page"] = ""; r["listed_email_on_page"] = ""
    b.close()
out = src.replace(".csv", "-verified.csv")
w = csv.DictWriter(open(out, "w", newline="", encoding="utf-8"), fieldnames=list(rows[0].keys()))
w.writeheader(); w.writerows(rows)
print("checked %d pages -> %s" % (len(rows), out))
