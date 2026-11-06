#!/usr/bin/env python3
"""
RECEIPTS CAMERA. Plain English: takes proof photos of everything our desks
published today, from GitHub's servers (which can reach the live web).

What it does:
  1. Builds the list of today's items: our stories in the Newswire Hollywood,
     Hollywood News Access, Gospel News Access and PR STARPOWER feeds dated
     on or after --since, plus any extra URLs in runbook/receipts/extra-urls.txt.
  2. Opens each live page in a real browser and saves a screenshot, plus the
     HTTP status and the time it was taken.
  3. For every Facebook/Instagram post in data/social-posted.json since that
     time, asks Meta's Graph API for the post's permalink and time (proof the
     post exists), then screenshots the public permalink.
  4. Writes everything to runbook/receipts/<slug>/ and receipts.json.

Needs: META_TOKEN secret for step 3 (without it, step 3 is skipped and
marked). Cost: zero (free Actions minutes on a public repo).
"""
import json, os, re, sys, urllib.request, urllib.parse, email.utils
from datetime import datetime, timezone
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH = "https://graph.facebook.com/v27.0"
FEEDS = {"Newswire Hollywood": "https://newswirehollywood.com/feed.xml",
         "Hollywood News Access": "https://hollywoodnewsaccess.com/feed.xml",
         "Gospel News Access": "https://gospelnewsaccess.com/feed.xml",
         "PR STARPOWER": "https://prstarpower.com/feed.xml"}
UA = "NewswireHollywoodReceipts/1.0 (+https://newswirehollywood.com)"

def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default

SINCE = arg("--since", datetime.now(timezone.utc).strftime("%Y-%m-%d"))
SLUG = arg("--slug", "receipts-" + SINCE)
OUT = os.path.join(ROOT, "runbook", "receipts", SLUG)
os.makedirs(OUT, exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

def feed_items():
    items = []
    for brand, url in FEEDS.items():
        try:
            root = ET.fromstring(get(url))
        except Exception as e:
            items.append({"brand": brand, "url": url, "error": "feed unreadable: %s" % e})
            continue
        for it in root.iter("item"):
            pd = it.findtext("pubDate") or ""
            try:
                d = email.utils.parsedate_to_datetime(pd).astimezone(timezone.utc).strftime("%Y-%m-%d")
            except Exception:
                d = ""
            if d >= SINCE:
                items.append({"brand": brand, "title": it.findtext("title"), "url": it.findtext("link"), "published": pd})
    extra = os.path.join(ROOT, "runbook", "receipts", "extra-urls.txt")
    if os.path.exists(extra):
        for line in open(extra, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#"):
                label, _, u = line.rpartition(" ")
                items.append({"brand": "extra", "title": label or u, "url": u})
    seen, out = set(), []
    for i in items:
        if i["url"] not in seen:
            seen.add(i["url"]); out.append(i)
    return out

def token():
    # Same key clean-up as scripts/social_post.py (the poster that works).
    lines = [l.strip() for l in os.environ.get("META_TOKEN", "").splitlines()]
    lines = [l for l in lines if l and l.lower() != "debug"]
    raw = re.sub(r"[^A-Za-z0-9]", "", "".join(lines))
    if raw.endswith("Debug"):
        raw = raw[:-5]
    m = re.search(r"EAA[A-Za-z0-9]{40,}", raw)
    return m.group(0) if m else raw

def social_posts():
    st = json.load(open(os.path.join(ROOT, "data", "social-posted.json"), encoding="utf-8"))
    rows = []
    for brand, d in st.get("posted", {}).items():
        for link, rec in d.items():
            if isinstance(rec, dict) and rec.get("at", "") >= SINCE:
                rows.append(dict(rec, brand=brand, story=link))
    for qid, rec in st.get("queue", {}).items():
        if isinstance(rec, dict) and rec.get("at", "") >= SINCE:
            rows.append(dict(rec, story="queue:" + qid))
    return rows

def graph_check(rows):
    tok = token()
    if not tok:
        for r in rows:
            r["graph"] = "skipped: META_TOKEN not available"
        return
    try:
        pages = json.loads(get("%s/me/accounts?%s" % (GRAPH, urllib.parse.urlencode(
            {"fields": "id,access_token", "limit": "100", "access_token": tok}))))["data"]
    except Exception as e:
        print("Graph page list failed: %s" % e)
        pages = []
    ptok = {p["id"]: p["access_token"] for p in pages}
    for r in rows:
        fb = r.get("facebook")
        if fb and "_" in str(fb):
            pid = str(fb).split("_")[0]
            try:
                j = json.loads(get("%s/%s?%s" % (GRAPH, fb, urllib.parse.urlencode(
                    {"fields": "permalink_url,created_time", "access_token": ptok.get(pid, tok)}))))
                r["facebook_permalink"] = j.get("permalink_url"); r["facebook_created"] = j.get("created_time")
            except Exception as e:
                r["facebook_graph_error"] = str(e)[:120]
        ig = r.get("instagram")
        if ig and str(ig).isdigit():
            try:
                j = json.loads(get("%s/%s?%s" % (GRAPH, ig, urllib.parse.urlencode(
                    {"fields": "permalink,timestamp,media_type", "access_token": tok}))))
                r["instagram_permalink"] = j.get("permalink"); r["instagram_created"] = j.get("timestamp")
            except Exception as e:
                r["instagram_graph_error"] = str(e)[:120]

def shoot(targets):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1, user_agent="Mozilla/5.0 " + UA)
        for t in targets:
            name = re.sub(r"[^a-z0-9]+", "-", t["url"].lower().split("//")[-1])[:90].strip("-") + ".png"
            pg = ctx.new_page()
            try:
                resp = pg.goto(t["url"], wait_until="networkidle", timeout=45000)
                pg.wait_for_timeout(1500)
                pg.screenshot(path=os.path.join(OUT, name), full_page=False)
                t["http_status"] = resp.status if resp else None
                t["screenshot"] = "runbook/receipts/%s/%s" % (SLUG, name)
            except Exception as e:
                t["shot_error"] = str(e)[:160]
            t["checked_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            pg.close()
        b.close()

def main():
    pages = feed_items()
    posts = social_posts()
    graph_check(posts)
    targets = [p for p in pages if "url" in p and not p.get("error")]
    for r in posts:
        for k in ("facebook_permalink", "instagram_permalink", "facebook_url", "instagram_url"):
            if r.get(k):
                targets.append({"url": r[k], "title": "%s %s" % (r.get("brand"), k), "brand": r.get("brand")})
                if k.startswith("facebook"):
                    break
    # instagram: one per post
    shoot(targets)
    run = os.environ.get("GITHUB_SERVER_URL", "") + "/" + os.environ.get("GITHUB_REPOSITORY", "") + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "")
    out = {"since": SINCE, "generated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
           "actions_run": run, "pages": pages, "social_posts": posts, "screenshots": targets}
    json.dump(out, open(os.path.join(OUT, "receipts.json"), "w"), indent=1)
    print("Receipts: %d pages, %d social posts, %d screenshots" % (len(pages), len(posts), sum(1 for t in targets if t.get("screenshot"))))

if __name__ == "__main__":
    main()
