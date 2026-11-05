#!/usr/bin/env python3
"""
SOCIAL AUTO-POSTER: Newswire Hollywood, Hollywood News Access, Gospel News Access,
PR STARPOWER.

Plain English: reads each site's own news feed (our reporting only, never the
wire cards), finds stories that have not been posted yet, and posts each one to
that brand's Facebook Page and Instagram account through Meta's official API.

What it needs: the GitHub Secret META_TOKEN (Terry's long-lived Meta user
token for the "Newswire Auto Poster" app). Without it the script prints
"not configured" and does nothing. The token is never printed or saved.

Safety rules:
  - The first run only records what already exists. It posts nothing, so
    switching it on never floods the Pages with old stories.
  - At most 2 new stories per brand per run.
  - Instagram needs a photo; a story without one goes to Facebook only.
  - Every post is logged in data/social-posted.json as the receipt.

Run by hand to post the newest story on each site right away:
    python3 scripts/social_post.py --post-latest
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

GRAPH = "https://graph.facebook.com/v27.0"
STATE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "social-posted.json")
MAX_PER_RUN = 2

# page_match is matched against the Facebook Page name, case-insensitive.
BRANDS = [
    {"name": "Newswire Hollywood", "feed": "https://newswirehollywood.com/feed.xml",
     "page_match": "newswire hollywood", "site": "newswirehollywood.com",
     "tags": "#Hollywood #EntertainmentNews #NewswireHollywood"},
    {"name": "Hollywood News Access", "feed": "https://hollywoodnewsaccess.com/feed.xml",
     "page_match": "hollywood news access", "site": "hollywoodnewsaccess.com",
     "tags": "#Hollywood #CelebrityNews #HollywoodNewsAccess"},
    {"name": "Gospel News Access", "feed": "https://gospelnewsaccess.com/feed.xml",
     "page_match": "gospel news access", "site": "gospelnewsaccess.com",
     "tags": "#Gospel #GospelMusic #GospelNewsAccess"},
    {"name": "PR STARPOWER", "feed": "https://prstarpower.com/feed.xml",
     "page_match": "pr starpower", "site": "prstarpower.com",
     "tags": "#PRSTARPOWER #HollywoodPR #Publicity"},
]

NS = {"media": "http://search.yahoo.com/mrss/"}
UA = "NewswireHollywoodSocial/1.0 (+https://newswirehollywood.com)"


def http(method, url, params=None, timeout=30):
    data = None
    if params is not None:
        body = urllib.parse.urlencode(params).encode()
        if method == "GET":
            url = url + ("&" if "?" in url else "?") + body.decode()
        else:
            data = body
    req = urllib.request.Request(url, data=data, method=method, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        # Meta's error body explains the problem; it never contains the token.
        try:
            err = json.loads(e.read().decode()).get("error", {})
            msg = (err.get("message") or str(e.reason)).split(" ")[:6]
            raise RuntimeError("%s (code %s)" % (" ".join(msg), err.get("code")))
        except ValueError:
            raise RuntimeError("HTTP %s" % e.code)


def read_feed(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    items = []
    for it in root.iter("item"):
        img = it.find("media:content", NS)
        if img is None:
            img = it.find("enclosure")  # PR STARPOWER's feed carries its photo here
        items.append({
            "title": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "dek": (it.findtext("description") or "").strip(),
            "image": img.get("url") if img is not None else "",
        })
    return [i for i in items if i["link"]]


def load_state():
    try:
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def save_state(state):
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
        f.write("\n")


def caption(item, brand, for_instagram):
    dek = item["dek"]
    if len(dek) > 400:
        dek = dek[:397].rsplit(" ", 1)[0] + "..."
    lines = [item["title"], ""] + ([dek, ""] if dek and dek != item["title"] else [])
    if for_instagram:
        lines.append("Full story at %s (link in bio)" % brand["site"])
    lines.append(brand["tags"])
    return "\n".join(lines).strip()


def post_facebook(page, item, brand):
    msg = caption(item, brand, False)
    r = http("POST", "%s/%s/feed" % (GRAPH, page["id"]),
             {"message": msg, "link": item["link"], "access_token": page["access_token"]})
    return r.get("id", "")


def post_instagram(page, item, brand):
    ig = (page.get("instagram_business_account") or {}).get("id")
    if not ig or not item["image"]:
        return ""
    tok = page["access_token"]
    c = http("POST", "%s/%s/media" % (GRAPH, ig),
             {"image_url": item["image"], "caption": caption(item, brand, True), "access_token": tok})
    cid = c.get("id")
    for _ in range(10):  # Instagram processes the photo before it can publish
        st = http("GET", "%s/%s" % (GRAPH, cid), {"fields": "status_code", "access_token": tok})
        if st.get("status_code") == "FINISHED":
            break
        if st.get("status_code") == "ERROR":
            raise RuntimeError("Instagram could not process the photo")
        time.sleep(3)
    r = http("POST", "%s/%s/media_publish" % (GRAPH, ig), {"creation_id": cid, "access_token": tok})
    return r.get("id", "")


def main():
    post_latest = "--post-latest" in sys.argv
    # A key copied from a wrapped screen can pick up line breaks; remove them.
    # Copying from Meta's debugger can pick up line breaks and the "Debug"
    # button label; keep only the key's letters and digits.
    lines = [l.strip() for l in os.environ.get("META_TOKEN", "").splitlines()]
    lines = [l for l in lines if l and l.lower() != "debug"]
    raw = re.sub(r"[^A-Za-z0-9]", "", "".join(lines))
    if raw.endswith("Debug"):
        raw = raw[:-5]
    m = re.search(r"EAA[A-Za-z0-9]{40,}", raw)  # Meta keys always start with EAA
    token = m.group(0) if m else raw
    # Safe diagnostics only: length and shape, never the key itself.
    print("Key check: %d characters, starts with EAA: %s" % (len(token), token.startswith("EAA")))
    if not token:
        print("Social poster not configured: the META_TOKEN secret is missing. Nothing posted.")
        return 0

    pages = http("GET", "%s/me/accounts" % GRAPH, {
        "fields": "name,id,access_token,instagram_business_account{id,username}",
        "limit": "100", "access_token": token}).get("data", [])
    print("Meta connection OK. Pages this token can manage: %d" % len(pages))
    for p in pages:
        ig = (p.get("instagram_business_account") or {}).get("username")
        print("  - %s%s" % (p.get("name"), (" + Instagram @%s" % ig) if ig else " (no Instagram linked)"))

    state = load_state()
    first_run = state is None
    state = state or {"_note": "Receipt log of every story the social poster has handled.", "posted": {}}

    for brand in BRANDS:
        # Spaces are ignored, so "PRstarpower" still matches "pr starpower".
        key = brand["page_match"].replace(" ", "")
        page = next((p for p in pages if key in (p.get("name") or "").lower().replace(" ", "")), None)
        try:
            items = read_feed(brand["feed"])
        except Exception as e:
            print("%s: could not read feed (%s). Skipped." % (brand["name"], e))
            continue
        # A brand added later gets its own first run: old stories are recorded, not posted.
        brand_first = first_run or brand["name"] not in state["posted"]
        done = state["posted"].setdefault(brand["name"], {})
        new = [i for i in items if i["link"] not in done]
        if brand_first or post_latest:
            # Record the back catalogue so it is never posted later by surprise.
            keep = items[:1] if post_latest else []
            for i in items:
                if i not in keep and i["link"] not in done:
                    done[i["link"]] = {"title": i["title"], "status": "existing before poster started"}
            new = keep
            if not keep:
                print("%s: first run, recorded %d existing stories, posted nothing." % (brand["name"], len(items)))
                continue
        if not page:
            print("%s: no matching Facebook Page on this token. Skipped." % brand["name"])
            continue
        for item in new[:MAX_PER_RUN]:
            rec = {"title": item["title"], "at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
            try:
                rec["facebook"] = post_facebook(page, item, brand)
            except Exception as e:
                rec["facebook_error"] = str(e)
            try:
                rec["instagram"] = post_instagram(page, item, brand) or "skipped (no photo or no linked account)"
            except Exception as e:
                rec["instagram_error"] = str(e)
            done[item["link"]] = rec
            print("%s: %s -> %s" % (brand["name"], item["title"], {k: v for k, v in rec.items() if k != "title"}))

    save_state(state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
