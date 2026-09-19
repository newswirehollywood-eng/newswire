#!/usr/bin/env python3
"""
wire.py - the publishing engine for Newswire Hollywood.

WHAT THIS DOES, PLAIN ENGLISH
-----------------------------
Every time it runs it pulls the public RSS feeds of the trades, reads the
headline, summary, publish time and photo out of each feed item, sorts the
items into sections by keyword, and rewrites docs/index.html plus the seven
section pages from scratch. After this, nobody hand-types an index page again.

Three things it merges together on every page:

  1. ORIGINATED - our own reporting, read from data/originated.json. These sit
     above everything else and never expire on the wire timer. This manifest is
     what stops a regeneration from wiping our own journalism off the site.
  2. WIRE - headline cards built from the trades' own RSS feeds. Each card
     shows the outlet's name, credits the photo to that outlet, and links out
     to the original article on the outlet's own site. We do not reproduce
     their article text - just the headline, a short trailing summary, and the
     thumbnail the feed itself publishes. That is the aggregator model (Google
     News, Flipboard, SmartNews), not syndication, and it needs no licence
     because the feed is published for exactly this use.
  3. TAKEOVERS - date-gated event skins, read from data/event-takeovers.json.
     While today is inside a takeover's start..end window the banner and nav
     item appear on every page. The day after it ends they vanish on the next
     hourly run with nobody touching a file.

PHOTOS
------
Pulled in this order out of each feed item, exactly as the feed publishes them:
  media:content url=  ->  media:thumbnail url=  ->  enclosure url=  ->
  the first <img> inside content:encoded or description
If an item ships no image, the card gets a CSS gradient well. No card is ever
bare, and no image is ever invented, scraped from a stock library, or presented
as ours. Wire photos are always credited to the outlet that published them.

WHAT IT NEVER DOES
------------------
Never invents a headline, a date, a byline or a photo. An item with no
parseable publish date is dropped rather than guessed at. BREAKING and
EXCLUSIVE flags are only ever set when those words are genuinely in the
outlet's own headline.

HOW TO RUN IT
-------------
  python3 wire.py              - full run, writes the pages
  python3 wire.py --dry-run    - fetch and report, write nothing

Runs hourly in CI via .github/workflows/wire.yml, which also has a
"Run workflow" button for forcing a run. Cost is zero: stdlib Python only, no
dependencies to install, no AI model calls, free Actions minutes on a public
repo. Every run appends its feed results to runbook/wire-feed-status.md so
there is always a record of which feeds answered and which were dropped.
"""

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")
STATUS_LOG = os.path.join(ROOT, "runbook", "wire-feed-status.md")

# Los Angeles is UTC-7 in September (PDT). The site's dateline is LA time.
LA = timezone(timedelta(hours=-7))

WIRE_WINDOW_DAYS = 7          # house rule: wire items older than this drop off
FETCH_TIMEOUT = 20            # seconds per feed
MAX_PER_SECTION = 12
HOME_WIRE_COUNT = 12

USER_AGENT = (
    "NewswireHollywoodBot/1.0 (+https://newswirehollywood.com; "
    "RSS aggregation with attribution and outbound links)"
)

# Sections wire.py owns. Order matters: an item lands in the FIRST section
# whose keywords it matches, so nothing is double-posted.
SECTIONS = [
    ("film", "Film", "Premieres, festivals, and the fall awards runway.", [
        "box office", "film festival", "movie", "feature film", "screenplay",
        "director", "sundance", "cannes", "venice film", "toronto film",
        "telluride", "blockbuster", "sequel", "casting for the film",
        "imax", "theatrical release", "first look at the film",
    ]),
    ("television", "Television", "Series, streamers, showrunners, and the awards race.", [
        "emmy", "emmys", "tv series", "season 2", "season 3", "showrunner",
        "netflix series", "hbo", "peacock", "hulu", "renewed for", "cancelled after",
        "episode", "limited series", "tv show", "streaming series", "pilot order",
        "television academy",
    ]),
    ("music", "Music", "Records, tours, charts, and the business of the songbook.", [
        "album", "billboard chart", "grammy", "tour dates", "single", "record label",
        "spotify", "streaming royalties", "concert", "band", "rapper", "songwriter",
        "music publishing", "catalog sale", "residency", "setlist",
    ]),
    ("fashion", "Fashion", "Red carpets, runways, and the houses dressing the industry.", [
        "red carpet", "fashion week", "runway", "couture", "stylist", "best dressed",
        "gown", "designer", "met gala", "vogue", "wore custom",
    ]),
    ("deals", "Deals", "Talent, packaging, and the transactions behind the business.", [
        "acquisition", "acquires", "merger", "sold to", "deal with", "signs with",
        "lawsuit", "sues", "settlement", "ipo", "stake in", "buyout", "layoffs",
        "licensing deal", "rights to", "overall deal", "valuation", "earnings",
    ]),
    ("ai-tech", "AI & Big Tech", "How AI and the platforms are remaking production, distribution and labour.", [
        "artificial intelligence", " ai ", "ai-", "openai", "anthropic", "chatgpt",
        "claude", "generative", "deepfake", "machine learning", "algorithm",
        "silicon valley", "startup", "app", "software", "chip", "data center",
    ]),
    ("international", "International", "The industry beyond Los Angeles.", [
        "korea", "korean", "japan", "japanese", "china", "chinese", "bollywood",
        "india", "uk ", "british", "london", "france", "french", "germany",
        "italy", "spain", "brazil", "nigeria", "nollywood", "international box office",
        "global rollout", "berlin", "busan",
    ]),
]

SECTION_LOOKUP = {slug: (label, blurb, kws) for slug, label, blurb, kws in SECTIONS}

# Gradient wells for items that ship no photo. Built from the house palette,
# not from stock imagery - an honest graphic, not a fake picture.
GRADIENTS = [
    "linear-gradient(135deg,#3A0A16 0%,#12060A 55%,#D1002E 145%)",
    "linear-gradient(135deg,#2A2013 0%,#0F0C07 55%,#B8860B 140%)",
    "linear-gradient(160deg,#1A1A1A 0%,#0A0A0A 50%,#7A0019 130%)",
    "linear-gradient(200deg,#241C0A 0%,#100D05 55%,#8A6400 135%)",
]


# --------------------------------------------------------------------------
# fetching and parsing
# --------------------------------------------------------------------------

def fetch(url):
    """Return the raw feed text, or raise with a readable reason."""
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        raw = resp.read()
    if raw[:2] == b"\x1f\x8b":          # gzip, some hosts send it regardless
        import gzip
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", errors="replace")


def _tag(block, name):
    """Pull the text of the first <name>...</name> out of an item block."""
    m = re.search(r"<%s[^>]*>(.*?)</%s>" % (name, name), block, re.S | re.I)
    if not m:
        return ""
    text = m.group(1).strip()
    cdata = re.match(r"^<!\[CDATA\[(.*?)\]\]>$", text, re.S)
    if cdata:
        text = cdata.group(1)
    return text.strip()


# Things that appear in feeds looking like images but are not photographs:
# analytics pixels, share buttons, avatars, spacers. A card showing one of
# these looks broken, so they never count as the item's picture.
NOT_A_PHOTO = re.compile(
    r"(pixel|/stats?[/.]|track|beacon|feedburner|doubleclick|gravatar|"
    r"emoji|spacer|blank\.|1x1|avatar|badge|logo|button|icon)", re.I)


def looks_like_photo(url):
    if not url.startswith("http"):
        return False
    if NOT_A_PHOTO.search(url):
        return False
    if re.search(r"\.gif(\?|$)", url, re.I):
        return False
    return True


def _attr_url(block, pattern):
    """First url="..." on a tag matching pattern, if it looks like an image."""
    for m in re.finditer(pattern, block, re.I):
        url = html.unescape(m.group(1)).strip()
        if looks_like_photo(url):
            return url
    return ""


def extract_image(block):
    """Feed image, in the documented priority order. Empty string if none."""
    url = _attr_url(block, r"<media:content[^>]*\burl=[\"']([^\"']+)[\"']")
    if url:
        return url
    url = _attr_url(block, r"<media:thumbnail[^>]*\burl=[\"']([^\"']+)[\"']")
    if url:
        return url
    for m in re.finditer(r"<enclosure[^>]*>", block, re.I):
        tag = m.group(0)
        if re.search(r'type=["\']image/', tag, re.I) or not re.search(r'type=', tag, re.I):
            u = _attr_url(tag, r'\burl=["\']([^"\']+)["\']')
            if u and re.search(r"\.(jpe?g|png|webp)", u, re.I):
                return u
    for tag_name in ("content:encoded", "description", "content", "summary"):
        body = _tag(block, tag_name)
        if not body:
            continue
        for m in re.finditer(r'<img[^>]*\bsrc=["\']([^"\']+)["\']', html.unescape(body), re.I):
            if looks_like_photo(m.group(1)):
                return m.group(1)
    # Last resort: the first image URL published anywhere in the item. Feeds
    # carry thumbnails under tags we have not anticipated (media:group,
    # post-thumbnail, image href, og:image mirrors), and this catches those
    # without inventing anything - it is still only ever a URL the outlet
    # itself published in its own feed.
    for m in re.finditer(r'["\'(>\s](https?://[^"\'<>)\s]+\.(?:jpe?g|png|webp))', block, re.I):
        url = html.unescape(m.group(1))
        if looks_like_photo(url):
            return url
    return ""


def strip_tags(s, limit=210):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) > limit:
        cut = s[:limit].rsplit(" ", 1)[0]
        s = cut.rstrip(",.;:-") + "…"
    return s


def parse_date(block):
    raw = _tag(block, "pubDate") or _tag(block, "published") or _tag(block, "updated")
    if not raw:
        return None
    try:
        dt = parsedate_to_datetime(raw)
    except (TypeError, ValueError):
        try:
            dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def parse_feed(text, source_name):
    """Turn feed XML into item dicts. Regex-based on purpose: real trade feeds
    are frequently not strictly well-formed, and a parser that throws on one
    stray ampersand would cost us the whole outlet for that hour."""
    items = []
    blocks = re.findall(r"<item\b.*?</item>", text, re.S | re.I)
    if not blocks:
        blocks = re.findall(r"<entry\b.*?</entry>", text, re.S | re.I)
    for block in blocks:
        title = strip_tags(_tag(block, "title"), 160)
        link = _tag(block, "link")
        if not link:
            m = re.search(r'<link[^>]*\bhref=["\']([^"\']+)["\']', block, re.I)
            link = m.group(1) if m else ""
        link = html.unescape(link).strip()
        published = parse_date(block)
        if not title or not link.startswith("http") or published is None:
            continue        # no guessing: an item we cannot date, we do not run
        items.append({
            "title": title,
            "link": link,
            "summary": strip_tags(_tag(block, "description") or _tag(block, "content:encoded")),
            "published": published,
            "image": extract_image(block),
            "source": source_name,
        })
    return items


def diagnose_no_photos(text):
    """A feed that returns items but no photos is either publishing images in a
    shape we do not read, or not publishing them at all. Those need different
    fixes, so say which it is in the status log instead of leaving it a
    mystery."""
    first = re.search(r"<(item|entry)\b.*?</\1>", text, re.S | re.I)
    block = first.group(0) if first else text[:4000]
    found = [t for t in ("media:content", "media:thumbnail", "media:group",
                         "enclosure", "content:encoded", "<img")
             if t in block.lower()]
    if not found:
        return "feed publishes no image fields at all"
    urls = re.findall(r"https?://[^\"'<>)\s]+\.(?:jpe?g|png|webp|gif)", block, re.I)
    if urls and all(not looks_like_photo(u) for u in urls):
        return "only non-photo assets (%s)" % ", ".join(sorted(found))
    return "carries %s but no usable photo URL" % ", ".join(sorted(found))


def collect(feeds, dry_run=False):
    """Fetch every feed. Returns (items, per-feed status rows)."""
    items, status = [], []
    for feed in feeds:
        name, url = feed["name"], feed["url"]
        try:
            text = fetch(url)
        except urllib.error.HTTPError as e:
            status.append((name, url, "dropped", "HTTP %s" % e.code, 0, 0))
            continue
        except Exception as e:                      # timeouts, DNS, TLS, resets
            status.append((name, url, "dropped", type(e).__name__, 0, 0))
            continue
        parsed = parse_feed(text, name)
        if not parsed:
            status.append((name, url, "dropped", "no parseable items", 0, 0))
            continue
        with_photo = sum(1 for i in parsed if i["image"])
        note = "" if with_photo else diagnose_no_photos(text)
        status.append((name, url, "ok", note, len(parsed), with_photo))
        items.extend(parsed)
    return items, status


# --------------------------------------------------------------------------
# routing, flags, takeovers
# --------------------------------------------------------------------------

def classify(item):
    hay = (" " + item["title"] + " " + item["summary"] + " ").lower()
    for slug, _label, _blurb, keywords in SECTIONS:
        for kw in keywords:
            if kw in hay:
                return slug
    return None


def flags_for(item):
    """Only ever true when the outlet's own headline says so."""
    t = item["title"].lower()
    return {
        "breaking": bool(re.search(r"\bbreaking\b", t)),
        "exclusive": bool(re.search(r"\bexclusive\b", t)),
    }


def active_takeover(takeovers, today):
    for t in takeovers:
        start = datetime.strptime(t["start"], "%Y-%m-%d").date()
        end = datetime.strptime(t["end"], "%Y-%m-%d").date()
        if start <= today <= end:
            return t
    return None


# --------------------------------------------------------------------------
# HTML building blocks
# --------------------------------------------------------------------------

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


CSS = """:root{--ink:#000;--body:#2B2B2B;--paper:#FDFBF6;--rule:#D6D4D0;--rule-soft:#EDEBE8;--signal:#D1002E;--date:#B8860B;--flag:#F5C518;--hed:'Archivo Narrow',Arial Narrow,sans-serif;--txt:'Newsreader',Georgia,serif;--wrap:1180px}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--paper);color:var(--body);font-family:var(--txt);font-size:17px;line-height:1.55}
a{color:inherit;text-decoration:none}
a:focus-visible{outline:2px solid var(--signal);outline-offset:2px}
img{display:block;max-width:100%}
.wrap{max-width:var(--wrap);margin:0 auto;padding:0 18px}
.masthead{background:var(--ink);color:#fff;padding:18px 0 14px}
.brand{font-family:var(--hed);font-weight:700;font-size:34px;line-height:.95;letter-spacing:-.5px;text-transform:uppercase;display:block}
.brand em{font-style:normal;color:var(--signal)}
.standfirst{font-family:var(--hed);font-weight:500;font-size:12px;letter-spacing:.18em;color:#9A9A9A;margin-top:7px;text-transform:uppercase}
.dateline{font-family:var(--hed);font-weight:500;font-size:11px;letter-spacing:.08em;color:#6A6A6A;margin-top:6px}
.nav{background:var(--ink);border-top:1px solid #262626;overflow-x:auto}
.nav ul{display:flex;list-style:none;white-space:nowrap;gap:22px;padding:11px 18px;max-width:var(--wrap);margin:0 auto}
.nav a{font-family:var(--hed);font-weight:600;font-size:13.5px;letter-spacing:.06em;color:#E8E8E8;text-transform:uppercase}
.nav a:hover,.nav a.current{color:var(--signal)}
.takeover-banner{background:var(--signal);color:#fff;text-align:center;padding:9px 18px;font-family:var(--hed);font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase}
.takeover-banner a{color:#fff;border-bottom:1px solid rgba(255,255,255,.6)}
.carpet{background:var(--ink);border-top:3px solid var(--date);border-bottom:3px solid var(--date);overflow:hidden;padding:10px 0}
.carpet-track{display:flex;white-space:nowrap;font-family:var(--hed);font-weight:700;font-size:12.5px;letter-spacing:.32em;text-transform:uppercase;color:var(--date)}
.carpet-track span{padding:0 26px;flex:none}
.carpet-track span:not(:last-child)::after{content:'\\2726';margin-left:26px;color:var(--signal)}
.lede{position:relative;min-height:60vh;display:flex;align-items:flex-end;background:var(--ink);overflow:hidden;border-bottom:3px solid var(--ink)}
.lede>.wrap{width:100%}
.lede-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.62}
.lede-fill{position:absolute;inset:0}
.lede-shade{position:absolute;inset:0;background:linear-gradient(0deg,rgba(0,0,0,.92) 0%,rgba(0,0,0,.55) 45%,rgba(0,0,0,.15) 100%)}
.lede-copy{position:relative;padding:60px 0 38px;color:#fff;max-width:26em}
.lede h1{font-family:var(--hed);font-weight:700;font-size:clamp(2.5rem,6vw,5rem);line-height:.95;letter-spacing:-1.5px;color:#fff;margin:12px 0 14px}
.lede h1 a:hover{color:var(--flag)}
.lede p{font-size:19px;color:#E4E4E4;line-height:1.45;max-width:34em}
.lede .credit{font-family:var(--hed);font-size:11px;letter-spacing:.09em;text-transform:uppercase;color:#B0B0B0;margin-top:16px}
.tagrow{display:flex;flex-wrap:wrap;gap:7px;align-items:center}
.tag{font-family:var(--hed);font-weight:700;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;padding:4px 9px;background:var(--signal);color:#fff}
.tag.flag{background:var(--flag);color:#111}
.tag.ours{background:var(--date);color:#111}
h2.sect{font-family:var(--hed);font-weight:700;font-size:clamp(21px,4vw,30px);color:var(--ink);border-bottom:3px solid var(--ink);padding-bottom:8px;margin:48px 0 6px}
.sect-note{font-size:15.5px;color:#6A6A6A;margin-bottom:24px}
.grid{display:grid;grid-template-columns:1fr;gap:26px}
@media(min-width:620px){.grid{grid-template-columns:1fr 1fr}}
@media(min-width:1000px){.grid{grid-template-columns:repeat(4,1fr)}}
.card{display:flex;flex-direction:column;border-bottom:1px solid var(--rule);padding-bottom:16px}
.card .shot{position:relative;width:100%;padding-top:62%;margin-bottom:12px;overflow:hidden;background:var(--ink)}
.card .shot img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.card .shot .well{position:absolute;inset:0}
.card .shot .well::after{content:attr(data-outlet);position:absolute;left:14px;bottom:12px;right:14px;font-family:var(--hed);font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.62)}
.card h3{font-family:var(--hed);font-weight:600;font-size:19px;line-height:1.16;color:var(--ink);margin:9px 0 7px}
.card:hover h3{color:var(--signal)}
.card p{font-size:14.5px;line-height:1.48;color:#5A5A5A}
.card .credit{font-family:var(--hed);font-size:11.5px;letter-spacing:.04em;color:#8A8A8A;margin-top:10px}
.card .credit b{color:var(--ink);font-weight:600}
.empty{border-top:2px solid var(--rule);padding:26px 0;margin-top:26px;color:#6A6A6A;font-size:16px;max-width:44em}
.band{background:var(--ink);color:#fff;padding:36px 0;margin-top:56px}
.band h2{font-family:var(--hed);font-weight:700;font-size:clamp(22px,4.5vw,32px);margin-bottom:9px}
.band p{color:#B4B4B4;max-width:48em}
.band a{color:var(--date);border-bottom:1px solid var(--date)}
footer{border-top:3px solid var(--ink);padding:26px 0 46px;font-family:var(--hed);font-size:13px;color:#6A6A6A}
footer nav{display:flex;flex-wrap:wrap;gap:18px;margin-bottom:14px}
footer nav a{color:var(--ink);font-weight:600;letter-spacing:.05em;text-transform:uppercase;font-size:12.5px}
footer nav a:hover{color:var(--signal)}
.machine{font-size:12.5px;color:#8A8A8A;margin-top:10px;font-family:var(--hed)}"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700'
         '&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap" rel="stylesheet">')


def nav_html(current, takeover):
    items = [("index.html", "Home")]
    items += [(slug + ".html", label) for slug, label, _b, _k in SECTIONS if slug != "international"]
    items += [("international.html", "International"), ("calendar.html", "The Calendar")]
    rows = []
    for href, label in items:
        cls = ' class="current"' if href == current else ""
        rows.append("<li><a href=\"%s\"%s>%s</a></li>" % (href, cls, esc(label)))
    if takeover:
        rows.append('<li><a href="%s" style="color:var(--signal)">%s</a></li>'
                    % (esc(takeover["link"]), esc(takeover["nav_label"])))
    rows.append('<li><a href="wire.html">The Wire</a></li>')
    rows.append('<li><a href="pressroom.html">Press Room</a></li>')
    return '<nav class="nav"><ul>\n%s\n</ul></nav>' % "\n".join(rows)


def head_html(title, description, canonical):
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:type" content="website">
<link rel="canonical" href="%s">
<link rel="sitemap" type="application/xml" href="sitemap.xml">
%s
<style>
%s
</style>
</head>""" % (esc(title), esc(description), esc(title), esc(description),
               esc(canonical), FONTS, CSS)


def masthead_html(now_la):
    return """<header class="masthead"><div class="wrap">
<a class="brand" href="index.html">Newswire <em>Hollywood</em></a>
<div class="standfirst">The business behind the business</div>
<div class="dateline">Los Angeles, California &middot; %s</div>
</div></header>""" % now_la.strftime("%A, %B %-d, %Y")


def banner_html(takeover):
    if not takeover:
        return ""
    return ('<div class="takeover-banner"><a href="%s">%s &rarr;</a></div>'
            % (esc(takeover["link"]), esc(takeover["banner"])))


def carpet_html(takeover):
    if not takeover or not takeover.get("carpet"):
        return ""
    words = [esc(w) for w in takeover["carpet"]] * 2
    return ('<div class="carpet"><div class="carpet-track">%s</div></div>'
            % "".join("<span>%s</span>" % w for w in words))


def lede_html(item, is_ours):
    """Full-bleed hero. Real feed photo when the item has one, house gradient
    well when it does not - never a stock photo standing in for either."""
    if item.get("image"):
        backdrop = '<img class="lede-img" src="%s" alt="" loading="eager">' % esc(item["image"])
        credit = "Photo: %s" % esc(item["source"]) if not is_ours else ""
    else:
        backdrop = '<div class="lede-fill" style="background:%s"></div>' % GRADIENTS[0]
        credit = "" if is_ours else "No photo published in %s's feed" % esc(item["source"])
    if is_ours:
        tags = '<span class="tag ours">%s</span>' % esc(item.get("tag", "Newswire Hollywood"))
        link_open, link_close = '<a href="%s">' % esc(item["link"]), "</a>"
        credit_line = esc(item.get("byline", ""))
    else:
        f = flags_for(item)
        tags = ""
        if f["breaking"]:
            tags += '<span class="tag flag">Breaking</span>'
        if f["exclusive"]:
            tags += '<span class="tag flag">Exclusive</span>'
        tags += '<span class="tag">%s</span>' % esc(item["source"])
        link_open = '<a href="%s" target="_blank" rel="noopener">' % esc(item["link"])
        link_close = "</a>"
        bits = ["Reported by %s" % esc(item["source"])]
        if credit:
            bits.append(credit)
        credit_line = " &middot; ".join(bits)
    return """<section class="lede">
%s
<div class="lede-shade"></div>
<div class="wrap"><div class="lede-copy">
<div class="tagrow">%s</div>
<h1>%s%s%s</h1>
<p>%s</p>
<div class="credit">%s</div>
</div></div>
</section>""" % (backdrop, tags, link_open, esc(item["title"]), link_close,
                 esc(item.get("dek") or item.get("summary", "")), credit_line)


def card_html(item, index, is_ours=False):
    if item.get("image"):
        shot = '<div class="shot"><img src="%s" alt="" loading="lazy"></div>' % esc(item["image"])
    else:
        well = GRADIENTS[index % len(GRADIENTS)]
        label = esc(item["source"]) if not is_ours else "Newswire Hollywood"
        shot = ('<div class="shot"><div class="well" style="background:%s" data-outlet="%s"></div></div>'
                % (well, label))
    if is_ours:
        tags = '<span class="tag ours">%s</span>' % esc(item.get("tag", "Ours"))
        head = '<h3><a href="%s">%s</a></h3>' % (esc(item["link"]), esc(item["title"]))
        credit = '<div class="credit">%s</div>' % esc(item.get("byline", ""))
        body = esc(item.get("dek", ""))
    else:
        f = flags_for(item)
        tags = ""
        if f["breaking"]:
            tags += '<span class="tag flag">Breaking</span>'
        if f["exclusive"]:
            tags += '<span class="tag flag">Exclusive</span>'
        tags += '<span class="tag">%s</span>' % esc(item["section_label"])
        head = ('<h3><a href="%s" target="_blank" rel="noopener">%s</a></h3>'
                % (esc(item["link"]), esc(item["title"])))
        photo_credit = (" &middot; Photo: %s" % esc(item["source"])) if item.get("image") else ""
        credit = ('<div class="credit"><b>%s</b>%s &middot; <a href="%s" target="_blank" '
                  'rel="noopener">Read it there &rarr;</a></div>'
                  % (esc(item["source"]), photo_credit, esc(item["link"])))
        body = esc(item.get("summary", ""))
    return ('<article class="card">%s<div class="tagrow">%s</div>%s<p>%s</p>%s</article>'
            % (shot, tags, head, body, credit))


def footer_html(now_utc, feed_ok, feed_total):
    return """<footer><div class="wrap">
<nav>
<a href="index.html">Home</a>
<a href="calendar.html">The Calendar</a>
<a href="wire.html">The Wire</a>
<a href="pressroom.html">Press Room</a>
<a href="pressroom.html#advertise">Advertise</a>
<a href="pressroom.html#standards">Standards &amp; Corrections</a>
</nav>
<div>&copy; 2026 Newswire Hollywood. All rights reserved. Los Angeles, California.</div>
<div class="machine">Headline cards credited to another outlet are that outlet's reporting, shown
from their own public feed with their own photo and a link to the original. Our reporting carries a
Newswire Hollywood desk byline. Page rebuilt automatically %s UTC from %d of %d feeds.</div>
</div></footer>""" % (now_utc.strftime("%Y-%m-%d %H:%M"), feed_ok, feed_total)


# --------------------------------------------------------------------------
# page generation
# --------------------------------------------------------------------------

def build_index(ours, wire_items, takeover, now_la, now_utc, feed_ok, feed_total):
    lede_item, rest = None, list(wire_items)
    if takeover:
        for o in ours:
            if o["link"] == takeover["link"]:
                lede_item = dict(o)
                break
    if lede_item is None and ours:
        lede_item = dict(ours[0])
    lede_is_ours = lede_item is not None
    if lede_item is None and rest:
        lede_item, rest = rest[0], rest[1:]

    parts = [head_html(
        "Newswire Hollywood — Entertainment News, The Business Behind The Business",
        "Breaking entertainment news from Los Angeles: film, television, music, fashion, deals, "
        "and how AI is remaking the industry. Our own reporting plus the wire, updated hourly.",
        "https://newswirehollywood.com/")]
    parts.append("<body>")
    parts.append(masthead_html(now_la))
    parts.append(nav_html("index.html", takeover))
    parts.append(banner_html(takeover))
    parts.append(carpet_html(takeover))
    if lede_item:
        parts.append(lede_html(lede_item, lede_is_ours))
    parts.append('<main><div class="wrap">')

    others = [o for o in ours if not (lede_is_ours and o["link"] == lede_item["link"])]
    if others:
        parts.append('<h2 class="sect">Our reporting</h2>')
        parts.append('<p class="sect-note">Originated by Newswire Hollywood desks. '
                     'Every one of these is ours, reported and bylined.</p>')
        parts.append('<div class="grid">%s</div>'
                     % "".join(card_html(o, i, is_ours=True) for i, o in enumerate(others)))

    if rest:
        parts.append('<h2 class="sect">The wire</h2>')
        parts.append('<p class="sect-note">Headlines and photos from the trades\' own feeds, '
                     'credited to the outlet that reported them, linking straight to their story. '
                     'Refreshed hourly; anything older than seven days drops off on its own.</p>')
        parts.append('<div class="grid">%s</div>'
                     % "".join(card_html(it, i) for i, it in enumerate(rest[:HOME_WIRE_COUNT])))
    else:
        parts.append('<div class="empty">No wire items came back on the last run. '
                     'That means every feed was unreachable or returned nothing inside the '
                     'seven-day window &mdash; it does not mean the industry went quiet. '
                     'See runbook/wire-feed-status.md for which feeds answered.</div>')

    parts.append("</div></main>")
    parts.append("""<section class="band"><div class="wrap">
<h2>Standards &amp; corrections</h2>
<p>Sourcing, embargoes, image licensing and corrections are covered in our
<a href="pressroom.html#standards">editorial standards</a>. Wire cards credit and link to the outlet
that did the reporting; we do not republish their article text. Spotted an error?
<a href="pressroom.html#standards">Send it through the Press Room</a>.</p>
</div></section>""")
    parts.append(footer_html(now_utc, feed_ok, feed_total))
    parts.append("""<script type="application/ld+json">
{"@context":"https://schema.org","@type":"NewsMediaOrganization","name":"Newswire Hollywood","url":"https://newswirehollywood.com/","description":"Breaking entertainment news, the Hollywood events calendar, and industry intelligence from Los Angeles.","email":"news@newswirehollywood.com","address":{"@type":"PostalAddress","addressLocality":"Los Angeles","addressRegion":"CA","addressCountry":"US"},"publishingPrinciples":"https://newswirehollywood.com/pressroom.html#standards","correctionsPolicy":"https://newswirehollywood.com/pressroom.html#standards"}
</script>""")
    parts.append("</body>\n</html>")
    return "\n".join(p for p in parts if p) + "\n"


def build_section(slug, ours, wire_items, takeover, now_la, now_utc, feed_ok, feed_total):
    label, blurb, _kw = SECTION_LOOKUP[slug]
    title = "%s | Newswire Hollywood" % label
    lede_item = dict(ours[0]) if ours else (dict(wire_items[0]) if wire_items else None)
    lede_is_ours = bool(ours)
    rest = wire_items[1:] if (wire_items and not lede_is_ours) else wire_items

    parts = [head_html(title, "Newswire Hollywood's %s desk: %s" % (label, blurb),
                       "https://newswirehollywood.com/%s.html" % slug)]
    parts.append("<body>")
    parts.append(masthead_html(now_la))
    parts.append(nav_html(slug + ".html", takeover))
    parts.append(banner_html(takeover))
    if lede_item:
        parts.append(lede_html(lede_item, lede_is_ours))
    parts.append('<main><div class="wrap">')

    tail_ours = ours[1:]
    if tail_ours:
        parts.append('<h2 class="sect">Our %s reporting</h2>' % esc(label.lower()))
        parts.append('<div class="grid">%s</div>'
                     % "".join(card_html(o, i, is_ours=True) for i, o in enumerate(tail_ours)))

    if rest:
        parts.append('<h2 class="sect">%s on the wire</h2>' % esc(label))
        parts.append('<p class="sect-note">From the trades\' own feeds, credited and linked to '
                     'the outlet that reported it. Rebuilt hourly, seven-day window.</p>')
        parts.append('<div class="grid">%s</div>'
                     % "".join(card_html(it, i) for i, it in enumerate(rest[:MAX_PER_SECTION])))
    elif not ours:
        parts.append('<div class="empty">Nothing matched %s on the wire in the last seven days, '
                     'and our own %s coverage has not published yet. This page fills itself the '
                     'moment either one lands &mdash; nobody types into it by hand.</div>'
                     % (esc(label), esc(label.lower())))

    parts.append("</div></main>")
    parts.append(footer_html(now_utc, feed_ok, feed_total))
    parts.append("""<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"%s","description":"Newswire Hollywood's %s desk: %s","url":"https://newswirehollywood.com/%s.html","publisher":{"@type":"NewsMediaOrganization","name":"Newswire Hollywood"}}
</script>""" % (esc(title), esc(label), esc(blurb), slug))
    parts.append("</body>\n</html>")
    return "\n".join(p for p in parts if p) + "\n"


LABELS = {
    "community":  ("COMMUNITY",  "Local Los Angeles. Ours, or submitted by the organization named."),
    "syndicated": ("SYNDICATED", "Written elsewhere, carried here with attribution and a link out."),
    "sponsored":  ("SPONSORED",  "Paid placement. Labeled, and never selected or edited by the Newsroom."),
}
LABEL_ORDER = ["community", "syndicated", "sponsored"]


def wire_item_html(item):
    """One item on The Wire. The label is not decoration - a reader has to be able
    to tell in one glance who wrote this and whether anyone paid for it."""
    kind = item.get("type", "community")
    if kind not in LABELS:
        kind = "community"
    label = LABELS[kind][0]

    parts = ['<article class="wireitem">']
    parts.append('<span class="lbl %s">%s</span>' % (kind, label))
    parts.append("<h3>%s</h3>" % esc(item.get("headline", "")))

    if item.get("when_text") or item.get("where"):
        bits = [b for b in (item.get("when_text"), item.get("where")) if b]
        parts.append('<div class="whenwhere">%s</div>'
                     % " &middot; ".join(esc(b) for b in bits))

    if item.get("dek"):
        parts.append('<p class="dek">%s</p>' % esc(item["dek"]))

    for para in [p for p in item.get("body", "").split("\n") if p.strip()]:
        parts.append('<p class="para">%s</p>' % esc(para.strip()))

    meta = []
    if kind == "sponsored":
        payer = item.get("paid_by", "").strip()
        meta.append("<b>Paid content.</b> %s" % (
            ("Paid for by %s." % esc(payer)) if payer
            else "Paid placement, distributed on behalf of a client."))
    if item.get("source"):
        if item.get("source_url"):
            meta.append('Source: <a href="%s" target="_blank" rel="noopener"><b>%s</b></a>'
                        % (esc(item["source_url"]), esc(item["source"])))
        else:
            meta.append("Source: <b>%s</b>" % esc(item["source"]))
    if item.get("contact"):
        meta.append("Contact: %s" % item["contact"])
    if item.get("date"):
        meta.append("Filed %s" % esc(item["date"]))
    if meta:
        parts.append('<div class="wiremeta">%s</div>' % " &middot; ".join(meta))

    parts.append("</article>")
    return "".join(parts)


def build_wire(wire_data, takeover, now_la, now_utc, feed_ok, feed_total):
    """docs/wire.html, generated. It used to be hand-typed and carried nothing at
    all, so it sat empty with a frozen dateline. Now it is built from
    data/wire-items.json on every run like every other index page."""
    items = wire_data.get("items", [])
    email = wire_data.get("submissions_email", "").strip()
    title = "The Wire | Newswire Hollywood"
    desc = ("Local Los Angeles items, syndicated coverage carried with attribution, "
            "and clearly labeled sponsored releases.")

    parts = [head_html(title, desc, "https://newswirehollywood.com/wire.html")]
    parts.append("<body>")
    parts.append(masthead_html(now_la))
    parts.append(nav_html("wire.html", takeover))
    parts.append(banner_html(takeover))
    parts.append('<div class="wrap"><div class="hero">')
    parts.append('<span class="kicker">The Wire</span>')
    parts.append("<h1>The Wire</h1>")
    parts.append("<p>Local Los Angeles, and everything that reaches this site by a path "
                 "other than our own newsroom. Three kinds of item run here, each labeled "
                 "so you can tell them apart at a glance.</p>")
    parts.append("</div></div>")
    parts.append('<main><div class="wrap">')

    parts.append('<p class="sect-note">%s</p>' % " ".join(
        '<span class="lbl %s">%s</span> %s' % (k, LABELS[k][0], esc(LABELS[k][1]))
        for k in LABEL_ORDER))

    if items:
        ordered = sorted(
            items,
            key=lambda i: (LABEL_ORDER.index(i.get("type", "community"))
                           if i.get("type") in LABELS else 0,
                           "" if not i.get("date") else i["date"]),
            reverse=False)
        ordered = sorted(ordered, key=lambda i: i.get("date", ""), reverse=True)
        parts.append("".join(wire_item_html(i) for i in ordered))
    else:
        parts.append('<div class="empty">Nothing on the wire yet. Items added to '
                     'data/wire-items.json appear here on the next hourly run &mdash; '
                     'nobody types into this page by hand.</div>')

    if email:
        parts.append('<div class="submit">')
        parts.append("<h3>Submit to The Wire</h3>")
        parts.append("<p>Local organizations, venues and publicists: send releases, event "
                     "listings and community notices to "
                     '<a href="mailto:%s"><b>%s</b></a>.</p>' % (esc(email), esc(email)))
        parts.append("<p>Include a date, a location and a named contact we can reach. "
                     "We run local items free. Paid distribution is a separate service and "
                     "anything paid for is labeled as such on this page.</p>")
        parts.append("</div>")

    parts.append("</div></main>")
    parts.append(footer_html(now_utc, feed_ok, feed_total))
    parts.append("""<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"The Wire","description":"%s","url":"https://newswirehollywood.com/wire.html","publisher":{"@type":"NewsMediaOrganization","name":"Newswire Hollywood"}}
</script>""" % esc(desc))
    parts.append("</body>\n</html>")
    return "\n".join(p for p in parts if p) + "\n"


# --------------------------------------------------------------------------
# takeover sync on the hand-written pages
# --------------------------------------------------------------------------

def sync_takeover_markers(active_ids, now_la, dry_run=False):
    """The article pages, calendar, press room and wire page are hand-written and
    wire.py does not regenerate them. Their nav still has to gain and lose the
    takeover item on the same schedule, so each carries a marked block:

        <!-- TAKEOVER:id --> ...nav item... <!-- /TAKEOVER:id -->

    While the takeover is live the block holds the nav item. Once it expires the
    block is emptied - markers stay put as the anchor for the next takeover. This
    is why no takeover ever needs removing by hand.

    Same pass also restamps the dateline. Those pages carried a hand-typed date
    that nobody remembers to change, so the calendar and press room were reading
    eight days old on a live news site. Now every page says today."""
    touched = []
    dateline_re = re.compile(
        r'(<div class="dateline">Los Angeles, California &middot; )[^<]*(</div>)')
    today = now_la.strftime("%A, %B %-d, %Y")
    pattern = re.compile(r"<!-- TAKEOVER:([a-z0-9-]+) -->(.*?)<!-- /TAKEOVER:\1 -->", re.S)
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        with open(path, encoding="utf-8") as f:
            original = f.read()

        def replace(m):
            tid, inner = m.group(1), m.group(2)
            if tid in active_ids:
                want = active_ids[tid]
            else:
                want = ""
            return "<!-- TAKEOVER:%s -->%s<!-- /TAKEOVER:%s -->" % (tid, want, tid)

        updated = pattern.sub(replace, original)
        updated = dateline_re.sub(r"\g<1>" + today + r"\g<2>", updated)
        if updated != original:
            touched.append(name)
            if not dry_run:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated)
    return touched


def write_status_log(status, now_utc, kept, dropped_old):
    ok = [s for s in status if s[2] == "ok"]
    lines = ["", "## Run %s UTC" % now_utc.strftime("%Y-%m-%d %H:%M"), ""]
    lines.append("Feeds answered: %d of %d. Items kept inside the %d-day window: %d "
                 "(%d dropped as older)." % (len(ok), len(status), WIRE_WINDOW_DAYS,
                                             kept, dropped_old))
    lines.append("")
    lines.append("| Feed | Status | Items | With photo | Note |")
    lines.append("| --- | --- | --- | --- | --- |")
    for name, _url, state, note, count, photos in status:
        lines.append("| %s | %s | %d | %d | %s |" % (name, state, count, photos, note or "-"))
    with open(STATUS_LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------

def main():
    dry_run = "--dry-run" in sys.argv
    now_utc = datetime.now(timezone.utc)
    now_la = now_utc.astimezone(LA)

    with open(os.path.join(DATA, "feeds.json"), encoding="utf-8") as f:
        feeds = json.load(f)["feeds"]
    with open(os.path.join(DATA, "originated.json"), encoding="utf-8") as f:
        originated = json.load(f)["articles"]
    with open(os.path.join(DATA, "event-takeovers.json"), encoding="utf-8") as f:
        takeovers = json.load(f)["takeovers"]

    live = active_takeover(takeovers, now_la.date())

    items, status = collect(feeds, dry_run)
    feed_ok = sum(1 for s in status if s[2] == "ok")

    cutoff = now_utc - timedelta(days=WIRE_WINDOW_DAYS)
    fresh, dropped_old = [], 0
    seen_links = set()
    for it in items:
        if it["published"] < cutoff:
            dropped_old += 1
            continue
        if it["link"] in seen_links:
            continue
        seen_links.add(it["link"])
        fresh.append(it)
    fresh.sort(key=lambda i: i["published"], reverse=True)

    by_section = {slug: [] for slug, _l, _b, _k in SECTIONS}
    unrouted = []
    for it in fresh:
        slug = classify(it)
        if slug:
            it["section_label"] = SECTION_LOOKUP[slug][0]
            by_section[slug].append(it)
        else:
            it["section_label"] = "The Wire"
            unrouted.append(it)

    ours_by_section = {slug: [] for slug, _l, _b, _k in SECTIONS}
    ours_all = []
    for a in originated:
        entry = {
            "title": a["title"], "link": a["url"], "dek": a.get("dek", ""),
            "summary": a.get("dek", ""), "byline": a.get("byline", ""),
            "tag": a.get("tag", "Newswire Hollywood"), "source": "Newswire Hollywood",
            "image": a.get("image", ""), "date": a.get("date", ""),
        }
        ours_all.append(entry)
        if a.get("section") in ours_by_section:
            ours_by_section[a["section"]].append(entry)
    ours_all.sort(key=lambda a: a.get("date", ""), reverse=True)

    wire_data = {}
    wire_items_path = os.path.join(DATA, "wire-items.json")
    if os.path.exists(wire_items_path):
        try:
            with open(wire_items_path, encoding="utf-8") as f:
                wire_data = json.load(f)
        except (ValueError, OSError) as exc:
            # A typo in the JSON must not take the whole site build down with it.
            print("wire-items.json unreadable, skipping The Wire: %s" % exc)
            wire_data = {}

    home_wire = fresh[:HOME_WIRE_COUNT] if fresh else []
    pages = {"index.html": build_index(ours_all, home_wire, live, now_la, now_utc,
                                       feed_ok, len(status))}
    for slug, _label, _blurb, _kw in SECTIONS:
        pages[slug + ".html"] = build_section(slug, ours_by_section[slug], by_section[slug],
                                              live, now_la, now_utc, feed_ok, len(status))
    pages["wire.html"] = build_wire(wire_data, live, now_la, now_utc, feed_ok, len(status))

    written = []
    for name, content in pages.items():
        path = os.path.join(DOCS, name)
        existing = ""
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                existing = f.read()
        if existing == content:
            continue
        written.append(name)
        if not dry_run:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

    active_ids = {}
    if live:
        active_ids[live["id"]] = ('<li><a href="%s" style="color:var(--signal)">%s</a></li>'
                                  % (live["link"], live["nav_label"]))
    touched = sync_takeover_markers(active_ids, now_la, dry_run)

    if not dry_run:
        write_status_log(status, now_utc, len(fresh), dropped_old)

    print("feeds ok: %d/%d" % (feed_ok, len(status)))
    for name, _u, state, note, count, photos in status:
        print("  %-28s %-8s items=%-3d photos=%-3d %s" % (name, state, count, photos, note))
    print("wire items kept: %d (dropped as older than %d days: %d, unrouted: %d)"
          % (len(fresh), WIRE_WINDOW_DAYS, dropped_old, len(unrouted)))
    print("takeover active: %s" % (live["id"] if live else "none"))
    print("pages rewritten: %s" % (", ".join(written) if written else "none (no change)"))
    print("takeover markers updated on: %s" % (", ".join(touched) if touched else "none"))
    if dry_run:
        print("DRY RUN - nothing written")


if __name__ == "__main__":
    main()
