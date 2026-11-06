#!/usr/bin/env python3
"""Builds the Skull Fest receipts: runbook/receipts/skull-fest-blast.md (repo)
and an HTML page (for the private Artifact) from runbook/receipts/skull-fest-blast/receipts.json.
Usage: build_skull_fest_receipts.py <html_out_dir>"""
import json, os, sys, csv, html, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.join(ROOT, "runbook/receipts/skull-fest-blast")
d = json.load(open(os.path.join(R, "receipts.json")))
shots = {t["url"]: t for t in d["screenshots"]}
GH = "https://github.com/newswirehollywood-eng/newswire"
RUN18 = GH + "/actions/runs/42140786990/job/127640312478"
RUN21 = GH + "/actions/runs/42141082009/job/127641344253"
LOGS = {
 "pr-skvlk-fest-2026-coverage.html": (RUN18, "01:01:30Z Newswire Hollywood: PRESS RELEASE: Newswire Hollywood and Hollywood News Access to Cover SKVLK Fest 2026 in Los Angeles -> facebook 1482063578315642_122103756003533251, instagram 18107567207575061"),
 "pr-skvlk-fest-2026-media-advisory.html": (RUN18, "01:01:30Z Newswire Hollywood: MEDIA ADVISORY: Interviews With SKVLK Fest 2026 ... -> facebook 1482063578315642_122103756177533251, instagram 18452014252121669"),
 "queue:brand-verdict-reel-nwh": (RUN18, "01:01:30Z Queue brand-verdict-reel-nwh -> facebook 1147693297809980, instagram 18176422147455110"),
 "russell-brand-guilty-rape-sexual-assault-verdict.html": (RUN21, "01:03:46Z Newswire Hollywood: Russell Brand Found Guilty of Rape ... -> facebook 1482063578315642_122103758229533251, instagram 17896372245447456"),
 "godzilla-minus-zero-opening-weekend-box-office.html": (RUN21, "01:03:46Z Newswire Hollywood: Godzilla Minus Zero Stomps Into 3,254 Theaters ... -> facebook 1482063578315642_122103758415533251, instagram 18102903224454743"),
 "queue:skvlk26-hna-1": (RUN21, "01:03:46Z Queue skvlk26-hna-1 -> facebook 103046575359785_1429031582770585, instagram 17911843860563774"),
 "queue:skvlk26-prs-1": (RUN21, "01:03:46Z Queue skvlk26-prs-1 -> facebook 1345437525329241_122105475483531256, instagram 18111932312353049"),
}
DESK = lambda key: "Skull Fest Release Desk" if "skvlk" in key else ("Hot Now Desk" if any(k in key for k in ("russell","godzilla","ramayana","verdict")) else "AGFF / earlier desk")

def shot(url):
    t = shots.get(url) or {}
    return t.get("screenshot"), t.get("http_status"), t.get("checked_at")

# ---------- rows ----------
pages = []
LABEL = {"pr-skvlk-fest-2026-coverage.html": "Press release: Newswire Hollywood and Hollywood News Access to Cover SKVLK Fest 2026",
         "pr-skvlk-fest-2026-media-advisory.html": "Media advisory: SKVLK Fest 2026 interviews through PR STARPOWER"}
for p in d["pages"]:
    u = p["url"]; slug = u.rsplit("/", 1)[-1]
    s, code, at = shot(u)
    desk = "Skull Fest Release Desk" if ("skvlk" in u or p["brand"] == "extra") else "Hot Now Desk"
    pages.append(dict(what=LABEL.get(slug) or p.get("title") or u, desk=desk, url=u, at=at, code=code, shot=s,
                      status="ok" if code == 200 else "fail", note="HTTP %s" % code))
posts = []
for r in d["social_posts"]:
    key = r.get("story", "")
    if not key.startswith("queue:"):
        key = key.rsplit("/", 1)[-1]
    if key.startswith("queue:agff"):
        continue  # earlier AGFF desk, before this blast
    if "ramayana" in key and not r.get("facebook"):
        continue
    log = LOGS.get(key, (None, "see data/social-posted.json"))
    fb = r.get("facebook_permalink") or r.get("facebook_url")
    ig = r.get("instagram_permalink") or r.get("instagram_url")
    posts.append(dict(brand=r.get("brand"), item=r.get("title") or key, key=key, desk=DESK(key), at=r.get("at"),
        fb_id=r.get("facebook"), fb=fb, fb_created=r.get("facebook_created"), fb_shot=shot(fb)[0] if fb else None,
        ig_id=r.get("instagram"), ig=ig, ig_created=r.get("instagram_created"), ig_shot=shot(ig)[0] if ig else None,
        run=log[0], logline=log[1]))
desks = list(csv.DictReader(open(os.path.join(ROOT, "runbook/press-releases/skull-fest/news-desks-verified.csv"), encoding="utf-8")))
SEND = ["fox11news@fox.com","editors@deadline.com","THRnews@thr.com","news_tips@billboard.com","beeditors@blackenterprise.com","pr@abc7.com","publicaffairs@kjlhradio.com","power106info@power106.com"]
SRC = {"pr@abc7.com":"https://abc7.com/news/submit-press-releases/50414/","publicaffairs@kjlhradio.com":"https://www.kjlhradio.com/contact","power106info@power106.com":"https://www.power106.com/contact/"}
for r in desks:
    if r["email"]: SRC[r["email"]] = r["source_url"]
OUTLET = {"fox11news@fox.com":"FOX 11 Los Angeles","editors@deadline.com":"Deadline","THRnews@thr.com":"The Hollywood Reporter","news_tips@billboard.com":"Billboard","beeditors@blackenterprise.com":"Black Enterprise","pr@abc7.com":"ABC7 Los Angeles","publicaffairs@kjlhradio.com":"KJLH 102.3","power106info@power106.com":"Power 106"}

FAILS = [
 ("Releases on the PR STARPOWER newsroom (prstarpower.com)", "Not published", "This session was refused access to the matariterry-art/prstarpower-site repo. Releases are live on Newswire Hollywood and posted to PR STARPOWER's Facebook and Instagram instead."),
 ("Releases on hollywoodnewsaccess.com", "Not published", "Same refusal for the Hollywood-NewsAccess/hollywoodnewsaccess repo. Posted to Hollywood News Access's Facebook and Instagram instead."),
 ("Advisory email to 8 newsrooms", "Draft, not sent", "Ready in Terry's Gmail (matariterry@gmail.com) Drafts, subject 'MEDIA ADVISORY: SKVLK Fest 2026 Saturday in LA: interviews available'. Claude does not send press email from Terry's account without his tap."),
 ("Free release sites (PRLog, OpenPR, PR.com)", "Not submitted", "Each needs an account in Terry's name. Copy-paste box: runbook/press-releases/skull-fest/free-release-sites.md"),
 ("Facebook posts, public view", "Hidden from logged-out visitors", "Meta's Graph API confirms all Facebook posts exist with timestamps, but a logged-out browser sees 'This content isn't available right now'. Usually a Page age or country restriction, or Facebook blocking robots. Terry: open one link logged out on your phone to check."),
 ("SKVLK Fest reel embedded in releases", "Not available", "No Skull Fest reel from the Announcement Desk was on main or the other sites as of 01:20 UTC. Placeholder box on both release pages."),
 ("Announcement Desk items", "None found", "No Skull Fest stories, cards or reels from the Announcement Desk were published on main, prstarpower-site or hollywoodnewsaccess as of 01:20 UTC, so there are none to receipt."),
 ("Drive doc '9 — ADVISORY DESK MEMORY'", "Not updated", "The edit was refused by the session's safety check. The text to add is in runbook/press-releases/skull-fest/README.md."),
 ("Dolls Kill affiliate code", "None yet", "No code exists. The Dolls Kill link carries rel=sponsored. Return to lock: fee, code, 12-month content rights, recap data (Monetization Plan, Win #1)."),
 ("Terry quote in releases", "Awaiting OK", "Draft in runbook/press-releases/skull-fest/quote-for-approval.md. Releases are live without a quote."),
]

# ---------- markdown ----------
def md():
    o = ["# SKULL FEST BLAST: RECEIPTS", "",
         "Proof of everything published for SKVLK Fest 2026 on Nov 6, 2026, plus the Hot Now Desk's stories that went out in the same window.",
         "", "Last checked: %s by the Receipts camera ([Actions run](%s)). Screenshots: runbook/receipts/skull-fest-blast/." % (d["generated"], d["actions_run"]), "",
         "## Live pages", "", "| Item | Desk | URL | Checked (UTC) | Proof |", "|---|---|---|---|---|"]
    for p in pages:
        o.append("| %s | %s | %s | %s | HTTP %s, %s |" % (p["what"], p["desk"], p["url"], p["at"], p["code"], p["shot"]))
    o += ["", "## Social posts (Facebook + Instagram via Graph API)", "", "| Brand | Item | Desk | Posted | Facebook (ID, Graph time) | Instagram (ID, Graph time) | Actions run + log line |", "|---|---|---|---|---|---|---|"]
    for p in posts:
        o.append("| %s | %s | %s | %s | %s (%s) %s | %s (%s) %s | %s `%s` |" % (p["brand"], p["item"], p["desk"], p["at"], p["fb"] or "-", p["fb_created"] or "", p["fb_id"] or "", p["ig"] or "-", p["ig_created"] or "", p["ig_id"] or "", p["run"] or "", p["logline"]))
    o += ["", "## Email", "", "Status: DRAFT ready in Terry's Gmail, not sent. To: info@prstarpower.com. BCC (each address appears on the outlet's own page, verified by the Receipts camera at 01:15 UTC):", ""]
    for e in SEND: o.append("- %s: %s (source: %s)" % (OUTLET[e], e, SRC.get(e, "")))
    o += ["", "Left out: Variety tips@ (Variety deletes press releases sent there), individual staff addresses, and outlets whose pages list no desk address (form or phone only; see news-desks-verified.csv).", "",
          "## Not done or failed (red)", ""]
    for a, b, c in FAILS: o.append("- **%s: %s.** %s" % (a, b, c))
    o += ["", "## Also delivered", "", "- RSS: both releases in newswirehollywood.com/feed.xml", "- News sitemap and sitemap: both releases listed (Regenerate sitemaps run on push)", "- Homepage and Music section: both releases listed by wire.py",
          "- Photo cards: docs/img/skvlk-fest-2026-wide.jpg (1200x630) and skvlk-fest-2026-ig.jpg (1080x1350), Newswire Hollywood original graphics"]
    return "\n".join(o) + "\n"
open(os.path.join(ROOT, "runbook/receipts/skull-fest-blast.md"), "w").write(md())

# ---------- html ----------
out = sys.argv[1] if len(sys.argv) > 1 else None
if not out: sys.exit()
os.makedirs(os.path.join(out, "shots"), exist_ok=True)
def img(path):
    if not path: return ""
    name = os.path.basename(path)
    shutil.copy(os.path.join(ROOT, path), os.path.join(out, "shots", name))
    return "shots/" + name
e = html.escape
def a(u, label=None): return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (e(u), e(label or u.replace("https://", "")))
ok_pages = sum(1 for p in pages if p["status"] == "ok")
nposts = sum(1 for p in posts if p["fb_id"]) + sum(1 for p in posts if p["ig_id"])
rows_p = "".join('<tr><td><span class="pill ok">Live</span></td><td class="what">%s<div class="sub">%s</div></td><td class="u">%s</td><td class="num">%s</td><td>%s</td></tr>' % (
    e(p["what"]), e(p["desk"]), a(p["url"]), e((p["at"] or "").replace(" UTC", "")), ('<a href="%s" target="_blank"><img loading="lazy" src="%s" alt="Screenshot of %s"></a>' % (img(p["shot"]), img(p["shot"]), e(p["url"])) if p["shot"] else "-")) for p in pages)
def social_cell(kind, url, created, pid, sh):
    if not url: return '<td>-</td>'
    warn = '<span class="pill warn">Hidden logged out</span>' if kind == "fb" else '<span class="pill ok">Public</span>'
    return '<td>%s<div class="u">%s</div><div class="sub num">ID %s<br>Graph: %s</div>%s</td>' % (warn, a(url, "Open post"), e(str(pid)), e(created or "n/a"),
        ('<a href="%s" target="_blank"><img loading="lazy" src="%s" alt="Screenshot of the %s post"></a>' % (img(sh), img(sh), kind)) if sh else "")
rows_s = "".join('<tr><td class="what">%s<div class="sub">%s &middot; %s &middot; %s</div></td>%s%s<td class="log">%s<code>%s</code></td></tr>' % (
    e(p["item"]), e(p["brand"]), e(p["desk"]), e(p["at"] or ""), social_cell("fb", p["fb"], p["fb_created"], p["fb_id"], p["fb_shot"]),
    social_cell("ig", p["ig"], p["ig_created"], p["ig_id"], p["ig_shot"]), (a(p["run"], "Actions run") + "<br>") if p["run"] else "", e(p["logline"])) for p in posts)
rows_e = "".join('<li><b>%s</b> <span class="num">%s</span> <span class="sub">source %s</span></li>' % (e(OUTLET[x]), e(x), a(SRC.get(x, ""), "outlet page")) for x in SEND)
rows_f = "".join('<li><span class="pill bad">%s</span><div><b>%s</b><p>%s</p></div></li>' % (e(b), e(a_), e(c)) for a_, b, c in FAILS)
page = open(os.path.join(ROOT, "runbook/receipts/receipts-template.html"), encoding="utf-8").read()
for k, v in {"@@GEN@@": e(d["generated"]), "@@RUN@@": a(d["actions_run"], "Receipts camera run"), "@@NPAGES@@": str(ok_pages), "@@NPOSTS@@": str(nposts),
             "@@NFAIL@@": str(len(FAILS)), "@@PAGES@@": rows_p, "@@SOCIAL@@": rows_s, "@@EMAILS@@": rows_e, "@@FAILS@@": rows_f}.items():
    page = page.replace(k, v)
open(os.path.join(out, "skull-fest-receipts.html"), "w", encoding="utf-8").write(page)
print("built", ok_pages, nposts, len(FAILS))
