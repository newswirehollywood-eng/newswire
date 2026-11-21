#!/usr/bin/env python3
"""
wire.py - the publishing engine for World Newswire Press.

WHAT THIS DOES, PLAIN ENGLISH
-----------------------------
Every hour it reads the public RSS feeds of the world's newsrooms (listed in
data/feeds.json), takes each item's headline, link, time and photo, sorts the
items into our sections, and rewrites these pages from scratch:

  docs/index.html                      the homepage (World)
  docs/<section>.html                  Americas, Europe, Africa, Middle East,
                                       Asia-Pacific, Business, Entertainment,
                                       Faith & Culture
  docs/wire.html                       The Wire: every live headline
  docs/feed.xml                        our own stories as RSS

It also refreshes the shared header and footer (world clocks, navigation,
WORLD BRIEFING ticker, follow band) inside every hand-written page - press
room, tips, partners, about and each article - between the WNP:HEADER and
WNP:FOOTER markers. Everything outside those markers is left alone.

THE STANDING RULES IT ENFORCES
------------------------------
* Wire cards show another outlet's headline, their own feed photo credited to
  them, and a link out to their story. Never their article text.
* Our own stories come from data/originated.json. A story with no
  signed_off_by is HELD: it appears on no page, no feed, no sitemap.
* A story whose embargo time is still in the future is HELD the same way.
  Its page waits in drafts/ (wire.py moves it there if it finds it in docs/)
  and moves into docs/ on its own the first hourly run after the embargo
  lifts. The Press Room's release list follows the same two gates.
* Sponsored items carry a visible SPONSORED label.
* Nothing is invented. An item with no parseable date is dropped. If every
  feed fails, the last good wire (data/wire-items.json) is kept until it ages
  out, and the homepage says honestly that the wire is refreshing.

HOW TO RUN IT
-------------
  python3 wire.py              full run, writes the pages
  python3 wire.py --offline    skip the feeds, rebuild from what we have
  python3 wire.py --dry-run    fetch and report, write nothing

Cost: zero. Standard-library Python only, no AI calls, free GitHub Actions.
"""

import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
DATA = os.path.join(ROOT, "data")
STATUS_LOG = os.path.join(ROOT, "runbook", "wire-feed-status.md")

SITE = "https://worldnewswirepress.com"
NAME = "World Newswire Press"
TAGLINE = "Giving the world a voice"
EMAIL = "info@worldnewswirepress.com"

# Social accounts. Leave a constant empty and its button simply does not show.
INSTAGRAM = "https://www.instagram.com/worldnewswire/"
FACEBOOK = "https://www.facebook.com/profile.php?id=100069767259386"
YOUTUBE = ""   # add the channel URL here when it exists

WIRE_WINDOW_HOURS = 72        # wire items older than this drop off
FETCH_TIMEOUT = 20
MAX_PER_SECTION = 15
HOME_WIRE_COUNT = 9
TICKER_WIRE_COUNT = 12
USER_AGENT = ("WorldNewswirePressBot/1.0 (+https://worldnewswirepress.com; "
              "RSS headline aggregation with attribution and outbound links)")

# The world clocks bar: city label, IANA time zone.
CLOCKS = [
    ("Los Angeles", "America/Los_Angeles"), ("New York", "America/New_York"),
    ("London", "Europe/London"), ("Lagos", "Africa/Lagos"),
    ("Dubai", "Asia/Dubai"), ("New Delhi", "Asia/Kolkata"),
    ("Tokyo", "Asia/Tokyo"), ("Sydney", "Australia/Sydney"),
]

# Sections. slug -> (nav label, page title, blurb, hero image or None)
SECTIONS = [
    ("americas", "Americas", "The Americas",
     "From Canada to Patagonia: politics, people and power across two continents.",
     "img/region-americas.jpg"),
    ("europe", "Europe", "Europe",
     "The continent's capitals, conflicts and conversations, from the Atlantic to the Urals.",
     "img/region-europe.jpg"),
    ("africa", "Africa", "Africa",
     "Fifty-four nations, 1.4 billion voices: the stories shaping the world's youngest continent.",
     "img/region-africa.jpg"),
    ("middle-east", "Middle East", "Middle East",
     "The Gulf, the Levant and North Africa: diplomacy, conflict, energy and everyday life.",
     "img/region-middle-east.jpg"),
    ("asia-pacific", "Asia-Pacific", "Asia-Pacific",
     "From Delhi to Tokyo to Sydney: the region where most of humanity lives.",
     "img/region-asia-pacific.jpg"),
    ("business", "Business", "Business",
     "Markets, trade, energy and the deals moving the global economy.", None),
    ("entertainment", "Entertainment", "Entertainment",
     "Film, television, music and the culture industries of every continent.", None),
    ("faith-culture", "Faith & Culture", "Faith & Culture",
     "Belief, heritage and the ideas that bind communities together.", None),
]
SECTION = {s[0]: s for s in SECTIONS}
REGIONS = ["americas", "europe", "africa", "middle-east", "asia-pacific"]

# Feeds marked "world" are routed to the region whose place names appear most
# often in the headline and summary. No match: the item stays on the homepage
# and The Wire only.
REGION_WORDS = {
    "americas": ["united states", "u.s.", "us ", "america", "washington", "trump", "canada",
                 "ottawa", "mexico", "brazil", "argentina", "chile", "colombia", "peru",
                 "venezuela", "cuba", "haiti", "caribbean", "latin america", "ecuador",
                 "bolivia", "guatemala", "honduras", "panama", "jamaica", "puerto rico",
                 "new york", "california", "lula", "milei"],
    "europe": ["europe", "european", "eu ", "brussels", "uk ", "britain", "british",
               "london", "england", "scotland", "ireland", "france", "french", "paris",
               "germany", "german", "berlin", "italy", "rome", "spain", "madrid",
               "ukraine", "ukrainian", "kyiv", "russia", "russian", "moscow", "kremlin",
               "putin", "zelensky", "poland", "netherlands", "belgium", "sweden", "norway",
               "finland", "denmark", "greece", "portugal", "austria", "hungary", "romania",
               "serbia", "balkans", "nato", "estonia", "latvia", "lithuania", "switzerland",
               "starmer", "macron", "merz"],
    "africa": ["africa", "african", "nigeria", "lagos", "abuja", "kenya", "nairobi",
               "south africa", "johannesburg", "ethiopia", "sudan", "khartoum", "congo",
               "ghana", "senegal", "mali", "niger", "burkina", "somalia", "uganda",
               "tanzania", "rwanda", "cameroon", "zimbabwe", "mozambique", "angola",
               "morocco", "algeria", "tunisia", "libya", "sahel", "ivory coast",
               "zambia", "malawi", "gambia", "chad", "eritrea"],
    "middle-east": ["middle east", "israel", "israeli", "gaza", "west bank", "palestin",
                    "iran", "iranian", "tehran", "iraq", "baghdad", "syria", "damascus",
                    "lebanon", "beirut", "hezbollah", "hamas", "saudi", "riyadh", "yemen",
                    "houthi", "qatar", "doha", "uae", "dubai", "abu dhabi", "jordan",
                    "egypt", "cairo", "oman", "kuwait", "bahrain", "turkey", "turkiye",
                    "erdogan", "hormuz", "netanyahu", "gulf"],
    "asia-pacific": ["asia", "china", "chinese", "beijing", "shanghai", "hong kong",
                     "taiwan", "japan", "japanese", "tokyo", "korea", "seoul", "pyongyang",
                     "india", "indian", "delhi", "mumbai", "pakistan", "bangladesh",
                     "dhaka", "myanmar", "rohingya", "thailand", "vietnam", "philippines",
                     "manila", "indonesia", "jakarta", "malaysia", "singapore", "australia",
                     "australian", "sydney", "canberra", "new zealand", "pacific",
                     "afghanistan", "kabul", "sri lanka", "nepal", "cambodia", "xi jinping",
                     "modi", "shenzhen"],
}

GRADIENTS = [
    "linear-gradient(135deg,#0A1F3D 0%,#14808A 140%)",
    "linear-gradient(135deg,#061429 0%,#3E7A4C 150%)",
    "linear-gradient(160deg,#12305A 0%,#D9A93B 170%)",
    "linear-gradient(200deg,#0A1F3D 0%,#B4602F 170%)",
]


# --------------------------------------------------------------------------
# fetching and parsing (regex on purpose: real feeds are often not strict XML,
# and a parser that throws on one stray ampersand would lose a whole outlet)
# --------------------------------------------------------------------------

def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT) as resp:
        raw = resp.read()
    if raw[:2] == b"\x1f\x8b":
        import gzip
        raw = gzip.decompress(raw)
    return raw.decode("utf-8", errors="replace")


def _tag(block, name):
    m = re.search(r"<%s(?:\s[^>]*)?>(.*?)</%s>" % (name, name), block, re.S | re.I)
    if not m:
        return ""
    text = m.group(1).strip()
    cdata = re.match(r"^<!\[CDATA\[(.*?)\]\]>$", text, re.S)
    if cdata:
        text = cdata.group(1)
    return text.strip()


NOT_A_PHOTO = re.compile(
    r"(pixel|/stats?[/.]|track|beacon|feedburner|doubleclick|gravatar|emoji|"
    r"spacer|blank\.|1x1|avatar|badge|logo|button|icon)", re.I)


def looks_like_photo(url):
    return (url.startswith("http") and not NOT_A_PHOTO.search(url)
            and not re.search(r"\.gif(\?|$)", url, re.I))


def _attr_url(block, pattern):
    for m in re.finditer(pattern, block, re.I):
        url = html.unescape(m.group(1)).strip()
        if looks_like_photo(url):
            return url
    return ""


def extract_image(block):
    """The photo the outlet itself published in its feed. Never invented."""
    for pat in (r"<media:content[^>]*\burl=[\"']([^\"']+)[\"']",
                r"<media:thumbnail[^>]*\burl=[\"']([^\"']+)[\"']"):
        url = _attr_url(block, pat)
        if url:
            return url
    for m in re.finditer(r"<enclosure[^>]*>", block, re.I):
        u = _attr_url(m.group(0), r'\burl=["\']([^"\']+)["\']')
        if u and re.search(r"\.(jpe?g|png|webp)", u, re.I):
            return u
    for tag_name in ("content:encoded", "description", "content", "summary"):
        body = _tag(block, tag_name)
        for m in re.finditer(r'<img[^>]*\bsrc=["\']([^"\']+)["\']', html.unescape(body), re.I):
            if looks_like_photo(m.group(1)):
                return m.group(1)
    return ""


def strip_tags(s, limit=400):
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s[:limit]


def parse_date(block):
    raw = (_tag(block, "pubDate") or _tag(block, "dc:date")
           or _tag(block, "published") or _tag(block, "updated"))
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


def parse_feed(text, feed):
    items = []
    blocks = (re.findall(r"<item\b.*?</item>", text, re.S | re.I)
              or re.findall(r"<entry\b.*?</entry>", text, re.S | re.I))
    for block in blocks:
        title = strip_tags(_tag(block, "title"), 200)
        link = _tag(block, "link")
        if not link:
            m = re.search(r'<link[^>]*\bhref=["\']([^"\']+)["\']', block, re.I)
            link = m.group(1) if m else ""
        link = html.unescape(link).strip()
        published = parse_date(block)
        if not title or not link.startswith("http") or published is None:
            continue      # no guessing: an item we cannot date, we do not run
        # The summary is used ONLY for routing by place name. It is never shown.
        hint = strip_tags(_tag(block, "description") or _tag(block, "summary"))
        items.append({
            "title": title, "link": link, "published": published.isoformat(),
            "image": extract_image(block), "source": feed["name"],
            "section": route(feed.get("section", "world"), title + " " + hint),
        })
    return items


def route(feed_section, text):
    if feed_section != "world":
        return feed_section
    hay = " " + text.lower() + " "
    best, best_n = "world", 0
    for region in REGIONS:
        n = sum(hay.count(w) for w in REGION_WORDS[region])
        if n > best_n:
            best, best_n = region, n
    return best


def collect(feeds):
    items, status = [], []
    for feed in feeds:
        try:
            text = fetch(feed["url"])
        except urllib.error.HTTPError as e:
            status.append((feed, "dropped", "HTTP %s" % e.code, 0, 0))
            continue
        except Exception as e:                          # timeouts, DNS, TLS
            status.append((feed, "dropped", type(e).__name__, 0, 0))
            continue
        parsed = parse_feed(text, feed)
        if not parsed:
            status.append((feed, "dropped", "no parseable items", 0, 0))
            continue
        status.append((feed, "ok", "", len(parsed), sum(1 for i in parsed if i["image"])))
        items.extend(parsed)
    return items, status


def merge_wire(fresh, cached, now):
    """New items plus the last good ones, de-duplicated, inside the window."""
    cutoff = now - timedelta(hours=WIRE_WINDOW_HOURS)
    seen, out = set(), []
    for it in sorted(fresh + cached, key=lambda i: i["published"], reverse=True):
        key = it["link"].split("?")[0]
        if key in seen:
            continue
        if datetime.fromisoformat(it["published"]) < cutoff:
            continue
        if datetime.fromisoformat(it["published"]) > now + timedelta(hours=1):
            continue      # a feed stamped in the future is a feed error
        seen.add(key)
        out.append(it)
    return out


# --------------------------------------------------------------------------
# our own stories: the sign-off and embargo gates
# --------------------------------------------------------------------------

def parse_when(s):
    if not s:
        return None
    s = s.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        dt = datetime.strptime(s[:10], "%Y-%m-%d")
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def is_live(a, now):
    """The two hard stops. Both must pass or the story appears nowhere."""
    if not (a.get("signed_off_by") or "").strip():
        return False, "no signed_off_by"
    emb = parse_when(a.get("embargo"))
    if emb and emb > now:
        return False, "embargoed until %s" % emb.isoformat()
    return True, ""


def load_originated(now):
    with open(os.path.join(DATA, "originated.json"), encoding="utf-8") as f:
        articles = json.load(f)["articles"]
    live, held = [], []
    for a in articles:
        ok, why = is_live(a, now)
        (live if ok else held).append((a, why))
    live = [a for a, _ in live]
    live.sort(key=lambda a: parse_when(a.get("published") or a["date"]), reverse=True)
    return live, held


# --------------------------------------------------------------------------
# HTML building blocks
# --------------------------------------------------------------------------

def esc(s):
    return html.escape(s or "", quote=True)


FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;"
         "0,9..144,600;0,9..144,700;1,9..144,500&family=Inter:wght@400;500;600;700;800"
         "&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap")


def head_html(title, description, path, image="img/share-1200x630.jpg", og_type="website",
              ld=None, robots="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"):
    url = SITE + "/" + ("" if path == "index.html" else path)
    img = image if image.startswith("http") else SITE + "/" + image
    ld_html = ""
    for block in (ld or []):
        ld_html += '<script type="application/ld+json">%s</script>\n' % json.dumps(
            block, ensure_ascii=False, indent=1)
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta property="og:site_name" content="{name}">
<meta property="og:type" content="{ogt}">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{img}">
<meta name="theme-color" content="#0A1F3D">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{name}" href="{site}/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{fonts}">
<link rel="stylesheet" href="assets/site.css">
{ld}</head>
""".format(t=esc(title), d=esc(description), url=url, name=NAME, ogt=og_type, img=img,
           site=SITE, fonts=FONTS, ld=ld_html, robots=robots)


def clocks_html():
    lis = "".join(
        '<li data-tz="%s"><span class="city">%s</span><span class="time">'
        '<i class="dot"></i><span class="t">--:--</span></span></li>' % (tz, city)
        for city, tz in CLOCKS)
    return '<div class="clocks" aria-label="World clocks"><ul>%s</ul></div>' % lis


NAV = [("index.html", "World", "world")] + [
    (s[0] + ".html", s[1], s[0]) for s in SECTIONS] + [
    ("wire.html", "The Wire", "wire"), ("pressroom.html", "Press Room", "pressroom")]


def nav_html(current):
    lis = []
    for href, label, key in NAV:
        cls = []
        if key == current:
            cls.append("current")
        if key == "pressroom":
            cls.append("press")
        lis.append('<li><a href="%s"%s%s>%s</a></li>' % (
            href, ' class="%s"' % " ".join(cls) if cls else "",
            ' aria-current="page"' if key == current else "", esc(label)))
    return '<nav class="nav" aria-label="Sections"><ul>%s</ul></nav>' % "".join(lis)


def ticker_html(entries):
    if not entries:
        return ""
    links = "".join('<a href="%s"%s>%s%s</a>' % (
        esc(e["href"]), ' rel="noopener" target="_blank"' if e["href"].startswith("http") else "",
        esc(e["text"]), ' <span class="src">%s</span>' % esc(e["src"]) if e.get("src") else "")
        for e in entries)
    # The run of headlines is written twice so the loop is seamless.
    return ('<div class="ticker" role="region" aria-label="World briefing">'
            '<div class="label">WORLD BRIEFING</div><div class="rail"><div class="track">'
            '%s<span aria-hidden="true" style="display:contents">%s</span></div></div></div>'
            % (links, links))


def masthead_html(now):
    return """<header class="masthead">
<div class="globe" role="img" aria-label="The Earth seen from Apollo 17"></div>
<div class="wrap">
<a class="brand" href="index.html"><span class="w">World</span>Newswire <em>Press</em></a>
<p class="tagline">{tag}</p>
<p class="dateline"><b>{day}</b><span class="upd">Updated {time} UTC</span></p>
</div>
</header>""".format(tag=TAGLINE, day=now.strftime("%A, %B ") + str(now.day) + now.strftime(", %Y"),
                    time=now.strftime("%H:%M"))


def header_block(current, now, ticker):
    return ("<!-- WNP:HEADER START -->\n"
            '<a class="skip" href="#main">Skip to the news</a>\n'
            + clocks_html() + "\n" + masthead_html(now) + "\n" + nav_html(current) + "\n"
            + ticker_html(ticker) + "\n<!-- WNP:HEADER END -->")


IG_SVG = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">'
          '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/>'
          '<circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>')
FB_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3'
          'c-2.8 0-4.5 1.8-4.5 4.6V11H7v4h2.5v6h4v-6H17l.5-4h-4V8.8c0-.5.3-.8.5-.8z"/></svg>')
YT_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M23 7.2a3 3 0 0 0'
          '-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8'
          ' 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0'
          ' 0-.5-4.8zM9.8 15.1V8.9l5.8 3.1-5.8 3.1z"/></svg>')


def footer_block(now):
    socials = []
    if INSTAGRAM:
        socials.append('<a href="%s" rel="me noopener" target="_blank">%s Instagram</a>' % (INSTAGRAM, IG_SVG))
    if FACEBOOK:
        socials.append('<a href="%s" rel="me noopener" target="_blank">%s Facebook</a>' % (FACEBOOK, FB_SVG))
    if YOUTUBE:
        socials.append('<a href="%s" rel="me noopener" target="_blank">%s YouTube</a>' % (YOUTUBE, YT_SVG))
    region_links = "".join('<li><a href="%s.html">%s</a></li>' % (s, SECTION[s][1]) for s in REGIONS)
    return """<!-- WNP:FOOTER START -->
<section class="follow" aria-label="Follow us">
<div class="wrap">
<div><h2>Follow <em>World Newswire Press</em></h2>
<p>The day's world news, the stories behind it, and the voices too often left out.</p></div>
<div class="socials">{socials}</div>
</div>
</section>
<footer class="foot">
<div class="wrap">
<div class="foot-grid">
<div class="foot-brand"><b>World Newswire Press</b>
<p>{tag}. An independent global newsroom and wire service, part of the Newswire Hollywood media group.</p></div>
<div><h4>Regions</h4><ul><li><a href="index.html">World</a></li>{regions}</ul></div>
<div><h4>Coverage</h4><ul><li><a href="business.html">Business</a></li><li><a href="entertainment.html">Entertainment</a></li><li><a href="faith-culture.html">Faith &amp; Culture</a></li><li><a href="wire.html">The Wire</a></li><li><a href="feed.xml">RSS feed</a></li></ul></div>
<div><h4>Work with us</h4><ul><li><a href="pressroom.html">Press Room &amp; rates</a></li><li><a href="tips.html">Send us a tip</a></li><li><a href="partners.html">Correspondents &amp; partners</a></li></ul></div>
<div><h4>About</h4><ul><li><a href="about.html">Our mission</a></li><li><a href="about.html#standards">Standards &amp; corrections</a></li><li><a href="mailto:{email}">{email}</a></li></ul></div>
</div>
<div class="foot-base">
<span>&copy; {year} World Newswire Press. Wire headlines link to and are credited to the outlets that published them; we never republish their articles. Sponsored content is always labeled.</span>
<span>Earth imagery: NASA, public domain.</span>
</div>
</div>
</footer>
<script src="assets/site.js" defer></script>
<!-- WNP:FOOTER END -->""".format(socials="".join(socials), tag=TAGLINE, regions=region_links,
                                  email=EMAIL, year=now.year)


def page(title, description, path, current, body, now, ticker, **head_kw):
    return (head_html(title, description, path, **head_kw) + "<body>\n"
            + header_block(current, now, ticker) + '\n<main id="main">\n' + body
            + "\n</main>\n" + footer_block(now) + "\n</body>\n</html>\n")


# --------------------------------------------------------------------------
# cards
# --------------------------------------------------------------------------

def nice_date(a):
    dt = parse_when(a.get("published") or a["date"])
    return dt.strftime("%B ") + str(dt.day) + dt.strftime(", %Y")


def ago(iso, now):
    mins = int((now - datetime.fromisoformat(iso)).total_seconds() // 60)
    if mins < 60:
        return "%d min ago" % max(mins, 1)
    if mins < 60 * 24:
        return "%d hr ago" % (mins // 60)
    return "%d days ago" % (mins // 1440)


def kicker_html(a):
    bits = []
    if a.get("sponsored"):
        bits.append('<span class="pill sponsored">Sponsored</span>')
    if a.get("kind") == "release":
        bits.append('<span class="pill gold">Press release</span>')
    else:
        bits.append('<span class="pill">World Desk</span>')
    label = a.get("tag") or SECTION.get(a.get("section"), (None, "World"))[1]
    bits.append(esc(label))
    return '<span class="kicker">%s</span>' % " ".join(bits)


def ours_card(a):
    return """<article class="card">
<a class="shot" href="{u}"><img src="{img}" alt="{alt}" loading="lazy"></a>
<div class="body">{k}
<h3><a href="{u}">{t}</a></h3>
<p>{d}</p>
<span class="meta">{date} &middot; {by}</span>
</div>
</article>""".format(u=esc(a["url"]), img=esc(a["image"]), alt=esc(a.get("image_alt", "")),
                     k=kicker_html(a), t=esc(a["title"]), d=esc(a["dek"]),
                     date=nice_date(a), by=esc(a.get("byline_short", "World Desk")))


def wire_card(it, i, now):
    if it.get("image"):
        shot = ('<img src="%s" alt="" loading="lazy" referrerpolicy="no-referrer">'
                '<span class="photo-credit">Photo: %s</span>' % (esc(it["image"]), esc(it["source"])))
    else:
        shot = '<span class="well" style="background:%s">%s</span>' % (
            GRADIENTS[i % len(GRADIENTS)], esc(it["source"]))
    return """<article class="card wire">
<a class="shot" href="{l}" rel="noopener" target="_blank">{shot}</a>
<div class="body"><span class="src">{src}</span>
<h3><a href="{l}" rel="noopener" target="_blank">{t}</a></h3>
<span class="meta">{ago} &middot; <span class="out">Read at {src} &#8599;</span></span>
</div>
</article>""".format(l=esc(it["link"]), shot=shot, src=esc(it["source"]), t=esc(it["title"]),
                     ago=ago(it["published"], now))


def refresh_note(feed_count):
    return ('<div class="refresh-note" role="status"><span class="spin" aria-hidden="true"></span>'
            '<div><b>The wire is refreshing.</b> Live headlines from %d of the world&rsquo;s '
            'newsrooms, from the BBC and Al Jazeera to Africanews and the Japan Times, load here '
            'automatically every hour. Each one links to the outlet that published it. '
            '<a href="wire.html" style="text-decoration:underline">See the sources on The Wire</a>.</div></div>'
            % feed_count)


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def org_ld():
    return {
        "@context": "https://schema.org", "@type": "NewsMediaOrganization",
        "name": NAME, "url": SITE + "/", "slogan": TAGLINE,
        "logo": {"@type": "ImageObject", "url": SITE + "/img/logo-512.png", "width": 512, "height": 512},
        "email": EMAIL, "sameAs": [u for u in (INSTAGRAM, FACEBOOK, YOUTUBE) if u],
        "parentOrganization": {"@type": "Organization", "name": "Newswire Hollywood"},
        "publishingPrinciples": SITE + "/about.html#standards",
        "correctionsPolicy": SITE + "/about.html#corrections",
    }


def explore_html(credits):
    cards = []
    for slug in REGIONS:
        _, label, _, blurb, img = SECTION[slug]
        cards.append('<a class="region" href="%s.html"><img src="%s" alt="%s seen from space" loading="lazy">'
                     '<span class="lbl"><i>Explore</i><b>%s</b><span>%s</span></span></a>'
                     % (slug, img, esc(label), esc(label), esc(credits.get(img, {}).get("caption", ""))))
    return """<section class="explore" aria-labelledby="explore-h">
<div class="wrap">
<h2 class="band-title" id="explore-h">Explore <em>the world</em></h2>
<p class="band-sub">Five regions, one newsroom. Choose a part of the planet and see every story we and the world&rsquo;s newsrooms are following there.</p>
<div class="regions">{cards}</div>
<p class="band-credit">Images: NASA, public domain, via Wikimedia Commons.</p>
</div>
</section>""".format(cards="".join(cards))


VOICE_HTML = """<section class="voice" aria-labelledby="voice-h">
<div class="wrap">
<h2 class="band-title" id="voice-h">Giving the world <em style="color:var(--teal)">a voice</em></h2>
<p class="band-sub">The best stories start with someone who was there. Here is how to bring yours to World Newswire Press.</p>
<div class="voice-grid">
<a class="voice-card" href="tips.html"><span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 4h16v12H7l-3 3z"/></svg></span>
<h3>Send us a tip</h3><p>Seen something the world should know? Tell our editors in confidence. Nothing is stored on this website.</p><span class="go">Send a confidential tip &rarr;</span></a>
<a class="voice-card gold" href="partners.html"><span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg></span>
<h3>Become a correspondent</h3><p>Reporters, photographers and stringers on every continent: pitch us, and we agree terms in writing before any assignment.</p><span class="go">Join the network &rarr;</span></a>
<a class="voice-card earth" href="pressroom.html"><span class="ic"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 5h16v14H4zM8 9h8M8 13h8M8 17h5"/></svg></span>
<h3>Press Room &amp; rates</h3><p>Distribute your news release worldwide. Clear tiers from $99, clearly labeled, carried on our wire and feed.</p><span class="go">See distribution tiers &rarr;</span></a>
</div>
</div>
</section>"""


def build_index(ours, wire, now, ticker, credits, feed_count):
    news = [a for a in ours if a.get("kind") != "release"]
    lead = next((a for a in ours if a.get("lead")), news[0] if news else (ours[0] if ours else None))
    rest = [a for a in ours if a is not lead]
    side, more = rest[:3], rest[3:]
    body = ['<div class="wrap">']
    if lead:
        side_html = "".join("""<article><div>{k}<h3><a href="{u}">{t}</a></h3><span class="meta">{date}</span></div>
<a class="thumb" href="{u}"><img src="{img}" alt="{alt}" loading="lazy"></a></article>""".format(
            k=kicker_html(a), u=esc(a["url"]), t=esc(a["title"]), date=nice_date(a),
            img=esc(a["image"]), alt=esc(a.get("image_alt", ""))) for a in side)
        body.append("""<section class="top" aria-label="Top stories">
<article class="lead">
<a class="shot" href="{u}"><img src="{img}" alt="{alt}" fetchpriority="high"></a>
<p class="credit">{credit}</p>
<div class="copy">{k}
<h2><a href="{u}">{t}</a></h2>
<p class="dek">{d}</p>
<p class="meta">{by} &middot; {date}</p>
</div>
</article>
<aside class="side"><span class="label">Also from the World Desk</span>{side}</aside>
</section>""".format(u=esc(lead["url"]), img=esc(lead["image"]), alt=esc(lead.get("image_alt", "")),
                     credit=esc(lead.get("photo_credit", "")), k=kicker_html(lead),
                     t=esc(lead["title"]), d=esc(lead["dek"]), by=esc(lead.get("byline", "")),
                     date=nice_date(lead), side=side_html))
    if more:
        body.append('<div class="sect-head"><h2>More from the World Desk</h2></div><div class="grid">%s</div>'
                    % "".join(ours_card(a) for a in more[:6]))
    body.append('<div class="sect-head"><h2>From the world&rsquo;s newsrooms</h2><a href="wire.html">The Wire &rarr;</a></div>')
    if wire:
        body.append('<div class="grid">%s</div>' % "".join(
            wire_card(it, i, now) for i, it in enumerate(wire[:HOME_WIRE_COUNT])))
    else:
        body.append(refresh_note(feed_count))
    # Region rows only when the wire has something for that region.
    for slug in REGIONS + ["business", "entertainment", "faith-culture"]:
        rows = [it for it in wire if it["section"] == slug][:4]
        if len(rows) >= 2:
            body.append('<div class="sect-head"><h2>%s</h2><a href="%s.html">More %s &rarr;</a></div>'
                        '<div class="grid four">%s</div>' % (
                            esc(SECTION[slug][1]), slug, esc(SECTION[slug][1]),
                            "".join(wire_card(it, i, now) for i, it in enumerate(rows))))
    body.append("</div>")
    body.append(explore_html(credits))
    body.append(VOICE_HTML)
    return page("World Newswire Press | World News, Giving the World a Voice",
                "World news from every region: the Americas, Europe, Africa, the Middle East and "
                "Asia-Pacific, plus business, entertainment and faith. Giving the world a voice.",
                "index.html", "world", "\n".join(body), now, ticker,
                ld=[org_ld(), {"@context": "https://schema.org", "@type": "WebSite",
                               "name": NAME, "url": SITE + "/"}])


def build_section(slug, ours, wire, now, ticker, credits, feed_count):
    _, label, title, blurb, img = SECTION[slug]
    mine = [a for a in ours if a.get("section") == slug]
    theirs = [it for it in wire if it["section"] == slug][:MAX_PER_SECTION]
    hero_img = ('<img src="%s" alt="">' % img) if img else ""
    style = "" if img else ' style="background:%s"' % GRADIENTS[REGIONS.__len__() % 4]
    cap = credits.get(img, {}).get("credit", "") if img else ""
    body = ["""<section class="sect-hero"{style}>{img}<div class="shade"></div>
<div class="wrap"><span class="kicker" style="color:var(--gold)">World Newswire Press</span>
<h1>{t}</h1><p>{b}</p>{cap}</div></section><div class="wrap">""".format(
        style=style, img=hero_img, t=esc(title), b=esc(blurb),
        cap=('<p class="credit">Image: %s</p>' % esc(cap)) if cap else "")]
    if mine:
        body.append('<div class="sect-head"><h2>From the World Desk</h2></div><div class="grid">%s</div>'
                    % "".join(ours_card(a) for a in mine))
    body.append('<div class="sect-head"><h2>%s on the wire</h2><a href="wire.html">All headlines &rarr;</a></div>' % esc(label))
    if theirs:
        body.append('<div class="grid">%s</div>' % "".join(wire_card(it, i, now) for i, it in enumerate(theirs)))
    else:
        body.append(refresh_note(feed_count))
    body.append("</div>")
    return page("%s News | World Newswire Press" % label, blurb, slug + ".html", slug,
                "\n".join(body), now, ticker)


def build_wire(wire, feeds, now, ticker, status):
    ok = {s[0]["name"] for s in status if s[1] == "ok"}
    body = ["""<div class="page" style="max-width:1100px"><span class="kicker">Live headlines</span>
<h1>The Wire</h1>
<p class="lede">Every headline from the world&rsquo;s newsrooms that we follow, newest first. Each links to the outlet that published it, with that outlet&rsquo;s own photo credited to them. We never republish their articles.</p>"""]
    if wire:
        body.append('<div class="grid" style="margin-top:26px">%s</div>' % "".join(
            wire_card(it, i, now) for i, it in enumerate(wire[:120])))
    else:
        body.append('<div style="margin-top:22px">%s</div>' % refresh_note(len(feeds)))
    groups = {}
    for f in feeds:
        groups.setdefault(f.get("section", "world"), []).append(f)
    rows = []
    for key in ["world"] + [s[0] for s in SECTIONS]:
        if key not in groups:
            continue
        label = "World (routed by region)" if key == "world" else SECTION[key][1]
        names = ", ".join(esc(f["name"]) + (" &#10003;" if f["name"] in ok else "") for f in groups[key])
        rows.append("<li><b>%s:</b> %s</li>" % (esc(label) if key != "world" else label, names))
    body.append('<h2>The newsrooms we follow</h2><p class="note-small">%d public RSS feeds, checked every hour. '
                'A tick means the feed answered on the latest run.</p><ul class="ticks">%s</ul></div>'
                % (len(feeds), "".join(rows)))
    return page("The Wire: Live World Headlines | World Newswire Press",
                "Live world headlines from the BBC, Al Jazeera, the Guardian, NPR, DW, France 24 and more, "
                "each linked to the outlet that published it.", "wire.html", "wire",
                "\n".join(body), now, ticker)


def build_rss(ours, now):
    items = []
    for a in ours[:30]:
        link = SITE + "/" + a["url"]
        img = SITE + "/" + a["image"]
        items.append("""<item>
<title>{t}</title>
<link>{l}</link>
<guid isPermaLink="true">{l}</guid>
<pubDate>{p}</pubDate>
<dc:creator>{by}</dc:creator>
<category>{c}</category>
<description>{d}</description>
<media:content url="{img}" medium="image" type="image/jpeg">
<media:credit>{cr}</media:credit>
</media:content>
</item>""".format(t=esc(("SPONSORED: " if a.get("sponsored") else "") + a["title"]), l=link,
                  p=format_datetime(parse_when(a.get("published") or a["date"])),
                  by=esc(a.get("byline", NAME)), c=esc(SECTION.get(a.get("section"), (0, "World"))[1]),
                  d=esc(a["dek"]), img=img, cr=esc(a.get("photo_credit", ""))))
    return """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
<title>{n}</title>
<link>{s}/</link>
<atom:link href="{s}/feed.xml" rel="self" type="application/rss+xml"/>
<description>{tag}. World news from every region.</description>
<language>en</language>
<lastBuildDate>{b}</lastBuildDate>
<image><url>{s}/img/logo-512.png</url><title>{n}</title><link>{s}/</link></image>
{items}
</channel>
</rss>
""".format(n=NAME, s=SITE, tag=TAGLINE, b=format_datetime(now), items="\n".join(items))


# --------------------------------------------------------------------------
# hand-written pages: refresh only the shared header and footer
# --------------------------------------------------------------------------

GENERATED = {"index.html", "wire.html"} | {s[0] + ".html" for s in SECTIONS}
HEADER_RE = re.compile(r"<!-- WNP:HEADER START -->.*?<!-- WNP:HEADER END -->", re.S)
FOOTER_RE = re.compile(r"<!-- WNP:FOOTER START -->.*?<!-- WNP:FOOTER END -->", re.S)
RELEASES_RE = re.compile(r"<!-- WNP:RELEASES START -->.*?<!-- WNP:RELEASES END -->", re.S)


def releases_block(ours):
    """The Press Room's release list: live releases only, so a held or
    embargoed release never shows up here early."""
    rel = [a for a in ours if a.get("kind") == "release"][:20]
    if rel:
        lis = "".join('<li><a href="%s">%s</a><span class="meta">%s%s</span></li>' % (
            esc(a["url"]), esc(a["title"]), nice_date(a),
            " &middot; Sponsored" if a.get("sponsored") else "") for a in rel)
        inner = '<ul class="release-list">%s</ul>' % lis
    else:
        inner = '<p class="note-small">No releases yet.</p>'
    return "<!-- WNP:RELEASES START -->\n%s\n<!-- WNP:RELEASES END -->" % inner


def sync_chrome(now, ticker, dry_run, ours=()):
    touched = 0
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html") or name in GENERATED or name.startswith("_"):
            continue
        path = os.path.join(DOCS, name)
        text = open(path, encoding="utf-8").read()
        if "WNP:HEADER START" not in text:
            continue
        m = re.search(r'<meta name="wnp-section" content="([^"]+)"', text)
        current = m.group(1) if m else ""
        new = HEADER_RE.sub(lambda _m: header_block(current, now, ticker), text)
        new = FOOTER_RE.sub(lambda _m: footer_block(now), new)
        new = RELEASES_RE.sub(lambda _m: releases_block(ours), new)
        if new != text:
            touched += 1
            if not dry_run:
                open(path, "w", encoding="utf-8").write(new)
    return touched


DRAFTS = os.path.join(ROOT, "drafts")


def stage_drafts(ours, held, dry_run):
    """Embargoes are hard stops, so an article page that is not cleared yet
    must not sit in docs/ where anyone could open it. Held pages live in
    drafts/. When a story clears (signed off, embargo passed) its page moves
    into docs/ on the next run; if a live page loses its clearance it moves
    back out. Returns a list of what moved, for the log."""
    moved = []
    for a, _why in held:
        src = os.path.join(DOCS, a["url"])
        if os.path.exists(src):
            moved.append("held -> drafts/%s" % a["url"])
            if not dry_run:
                os.makedirs(DRAFTS, exist_ok=True)
                os.replace(src, os.path.join(DRAFTS, a["url"]))
    for a in ours:
        src = os.path.join(DRAFTS, a["url"])
        if os.path.exists(src) and not os.path.exists(os.path.join(DOCS, a["url"])):
            moved.append("released -> docs/%s" % a["url"])
            if not dry_run:
                os.replace(src, os.path.join(DOCS, a["url"]))
    return moved


def write(path, text, dry_run):
    if dry_run:
        return
    with open(os.path.join(DOCS, path), "w", encoding="utf-8") as f:
        f.write(text)


def write_status_log(status, now, kept, held):
    ok = sum(1 for s in status if s[1] == "ok")
    lines = ["# Wire feed status", "",
             "Rewritten by wire.py on every run. Plain English: which feeds answered on the latest run, "
             "which were dropped and why, and which of our stories are being held.", "",
             "Latest run: %s UTC. Feeds answering: %d of %d. Wire items on the site: %d." % (
                 now.strftime("%Y-%m-%d %H:%M"), ok, len(status), kept), "",
             "| Feed | Section | Result | Items | With photo |", "|---|---|---|---|---|"]
    for feed, state, note, n, photos in status:
        lines.append("| %s | %s | %s | %d | %d |" % (
            feed["name"], feed.get("section", "world"), state + (" (%s)" % note if note else ""), n, photos))
    lines += ["", "## Held stories (not on any page, feed or sitemap)", ""]
    lines += ["- %s: %s" % (a["url"], why) for a, why in held] or ["- none"]
    os.makedirs(os.path.dirname(STATUS_LOG), exist_ok=True)
    with open(STATUS_LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    dry_run = "--dry-run" in sys.argv
    offline = "--offline" in sys.argv
    now = datetime.now(timezone.utc).replace(microsecond=0)
    feeds = json.load(open(os.path.join(DATA, "feeds.json"), encoding="utf-8"))["feeds"]
    try:
        credits = json.load(open(os.path.join(DATA, "image-credits.json"), encoding="utf-8"))
    except OSError:
        credits = {}

    if offline:
        fresh, status = [], [(f, "skipped", "offline run", 0, 0) for f in feeds]
    else:
        fresh, status = collect(feeds)
    cache_path = os.path.join(DATA, "wire-items.json")
    try:
        cached = json.load(open(cache_path, encoding="utf-8"))["items"]
    except (OSError, ValueError, KeyError):
        cached = []
    wire = merge_wire(fresh, cached, now)

    ours, held = load_originated(now)

    ticker = [{"href": a["url"], "text": a["title"]} for a in ours[:8]]
    ticker += [{"href": it["link"], "text": it["title"], "src": it["source"]}
               for it in wire[:TICKER_WIRE_COUNT]]

    ok = sum(1 for s in status if s[1] == "ok")
    print("feeds answering: %d/%d | wire items: %d | our live stories: %d | held: %d"
          % (ok, len(feeds), len(wire), len(ours), len(held)))
    for a, why in held:
        print("  HELD %s - %s" % (a["url"], why))
    for line in stage_drafts(ours, held, dry_run):
        print("  " + line)
    if dry_run:
        return

    write("index.html", build_index(ours, wire, now, ticker, credits, len(feeds)), dry_run)
    for s in SECTIONS:
        write(s[0] + ".html", build_section(s[0], ours, wire, now, ticker, credits, len(feeds)), dry_run)
    write("wire.html", build_wire(wire, feeds, now, ticker, status), dry_run)
    write("feed.xml", build_rss(ours, now), dry_run)
    n = sync_chrome(now, ticker, dry_run, ours)
    print("hand-written pages refreshed: %d" % n)
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump({"_note": "Last good wire items, so a run where every feed fails does not blank the site. "
                            "Rewritten by wire.py every run.", "items": wire}, f, indent=1)
    write_status_log(status, now, len(wire), held)


if __name__ == "__main__":
    main()
