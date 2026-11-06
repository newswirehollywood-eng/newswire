#!/usr/bin/env python3
"""Builds the two SKVLK Fest 2026 release pages in docs/ from the AGFF release
template (same look, same labels). Rerun after editing the text below."""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TPL = open(os.path.join(ROOT, "docs/pr-agff-2026-global-film-awards-tonight.html"), encoding="utf-8").read()
head_css = TPL.split("<meta property=\"og:image\"")[0]   # everything up to the social block
head_css = re.sub(r"<title>.*?</title>", "<title>@@TITLE@@</title>", head_css, flags=re.S)
head_css = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="@@DESC@@">', head_css)
head_css = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="@@HED@@">', head_css)
head_css = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="@@URL@@">', head_css)
head_css = head_css.replace("</style>", ".reel{border:1px dashed var(--rule);padding:16px;font-family:var(--hed);font-size:14px;color:#6A6A6A;margin:0 0 30px}\n.qa dt{font-family:var(--hed);font-weight:700}\n</style>")
nav = TPL[TPL.index('<header class="masthead">'):TPL.index("<main>")]
nav = nav.replace("Thursday, November 5, 2026", "Friday, November 6, 2026")
nav = re.sub(r"<!-- TAKEOVER:emmys-2026 -->.*?<!-- /TAKEOVER:emmys-2026 -->\n", "", nav)

IMG = "https://newswirehollywood.com/img/skvlk-fest-2026-wide.jpg"
def page(slug, title, hed, desc, body):
    url = "https://newswirehollywood.com/" + slug
    h = head_css.replace("@@TITLE@@", title).replace("@@DESC@@", desc).replace("@@HED@@", hed).replace("@@URL@@", url)
    social = f"""<meta property="og:image" content="{IMG}">
<!-- SOCIAL -->
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Newswire Hollywood">
<meta property="article:published_time" content="2026-11-06">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="PRESS RELEASE: {hed}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{IMG}">
<!-- /SOCIAL -->
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"NewsArticle","headline":"{hed}","datePublished":"2026-11-06","image":["{IMG}"],"author":{{"@type":"Organization","name":"PR STARPOWER","url":"https://prstarpower.com"}},"publisher":{{"@type":"Organization","name":"Newswire Hollywood","url":"https://newswirehollywood.com"}},"mainEntityOfPage":"{url}"}}</script>
</head>
<body>

"""
    foot = """
</article>
</main>

<footer><div class="wrap">
<nav>
<a href="index.html">Home</a>
<a href="pressroom.html">Press Room</a>
<a href="pr-skvlk-fest-2026-coverage.html">SKVLK Fest coverage</a>
<a href="pr-skvlk-fest-2026-media-advisory.html">SKVLK Fest media advisory</a>
</nav>
<div>&copy; 2026 Newswire Hollywood. Los Angeles, California.</div>
</div></footer>

</body>
</html>
"""
    open(os.path.join(ROOT, "docs", slug), "w", encoding="utf-8").write(h + social + nav + "<main>\n<article class=\"art\">\n" + body + foot)

FIG = """<figure class="pr-img">
  <img src="img/skvlk-fest-2026-wide.jpg" alt="SKVLK Fest 2026, Saturday, Nov. 7, Los Angeles. Press release and media advisory card.">
  <figcaption>SKVLK Fest 2026. Graphic: Newswire Hollywood original. Available for editorial use. Instagram size: <a href="img/skvlk-fest-2026-ig.jpg" style="color:var(--signal)">1080 x 1350</a>.</figcaption>
</figure>
"""
REEL = """<div class="reel" id="reel">Video: the SKVLK Fest 2026 announcement reel will be embedded here when it is published.</div>
"""
GLANCE = """<div class="card"><div class="card-head">At a glance</div><div class="card-body"><dl>
<dt>Event</dt><dd>SKVLK Fest 2026, a youth-culture music and carnival festival</dd>
<dt>Date</dt><dd>Saturday, Nov. 7, 2026</dd>
<dt>Location</dt><dd>Los Angeles. A private location; details are shared with approved media only.</dd>
<dt>2025 by the numbers</dt><dd>25,000 guests, 15,000 more turned away at capacity, more than 100 million people reached (figures reported by the festival)</dd>
<dt>2025 performers</dt><dd>GloRilla, Tyga, Leon Thomas and YK Osiris (as reported by BET, Complex and XXL)</dd>
<dt>Sponsor</dt><dd>Dolls Kill, VIP Creator Lounge</dd>
<dt>Publicity and partnerships</dt><dd>PR STARPOWER &middot; <a href="https://prstarpower.com/skvlk-fest.html" style="color:var(--signal)">prstarpower.com/skvlk-fest.html</a></dd>
<dt>Media partners on site</dt><dd>Newswire Hollywood, Hollywood News Access, and Billboard among other outlets</dd>
</dl></div></div>
"""
ABOUT = """<h2>About SKVLK Fest</h2>
<p>SKVLK Fest is a Los Angeles youth-culture music and carnival festival founded by Anelise, the daughter of Academy Award winner Jamie Foxx. Its 2025 edition drew 25,000 guests and reached more than 100 million people, according to the festival.</p>

<h2>About Newswire Hollywood</h2>
<p>Newswire Hollywood is an entertainment news organization and wire service in Los Angeles covering film, television, music, fashion, deals and the business of the industry. <a href="https://newswirehollywood.com" style="color:var(--signal)">newswirehollywood.com</a></p>

<h2>About Hollywood News Access</h2>
<p>Hollywood News Access covers celebrity news, red carpets, music, television and movies from Hollywood, updated around the clock. <a href="https://hollywoodnewsaccess.com" style="color:var(--signal)">hollywoodnewsaccess.com</a></p>

<h2>About PR STARPOWER</h2>
<p>PR STARPOWER is a Los Angeles public relations firm representing talent, productions and events in entertainment, faith and culture. It leads sponsorship, brand partnerships and publicity for SKVLK Fest and produces the festival&rsquo;s VIP Creator Lounge. <a href="https://prstarpower.com" style="color:var(--signal)">prstarpower.com</a></p>

<div class="ends">###</div>

<div class="contact">
  <p style="margin-bottom:10px"><b>MEDIA CONTACT</b></p>
  <p style="margin-bottom:4px">Terry Bryant &middot; Lead Publicist, PR STARPOWER</p>
  <p style="margin-bottom:0"><a href="mailto:info@prstarpower.com?subject=SKVLK%20Fest%202026%20Media%20Request" style="color:var(--signal)">info@prstarpower.com</a> &middot; 646-315-2942</p>
</div>

<p style="font-family:var(--hed);font-size:13px;color:#7A7A7A;border-top:1px solid var(--rule);padding-top:16px">Disclosure: this release is issued by PR STARPOWER, which leads sponsorship, partnerships and publicity for SKVLK Fest and is paid for that work. PR STARPOWER, Newswire Hollywood and Hollywood News Access are sister companies. Dolls Kill is the sponsor of the festival&rsquo;s VIP Creator Lounge. Newswire Hollywood&rsquo;s editorial coverage is produced independently.</p>

<p><a href="pressroom.html" style="color:var(--signal);font-weight:600">Press Room &rsaquo;</a></p>
"""

# ---------- RELEASE A ----------
hedA = "Newswire Hollywood and Hollywood News Access to Cover SKVLK Fest 2026 in Los Angeles"
dekA = "The entertainment outlets will report live from Saturday&rsquo;s youth-culture music and carnival festival alongside Billboard and other major media, including the Dolls Kill-styled VIP Creator Lounge."
bodyA = f"""<span class="prlabel">Press release &middot; Issued by PR STARPOWER</span>
<div class="prmeta">FOR IMMEDIATE RELEASE &nbsp;&middot;&nbsp; Los Angeles &nbsp;&middot;&nbsp; Nov. 6, 2026</div>

<h1 style="margin-top:0">{hedA}</h1>

<p class="dek">{dekA}</p>

{FIG}{REEL}
<p><b>LOS ANGELES (Nov. 6, 2026) &mdash;</b> <b>Newswire Hollywood</b> and <b>Hollywood News Access</b> will be on the ground Saturday, Nov. 7, to cover <b>SKVLK Fest 2026</b>, the Los Angeles youth-culture music and carnival festival that drew 25,000 guests last year and turned away 15,000 more at capacity, according to the festival.</p>

<p>The two outlets join <b>Billboard</b> and other major media at the festival, with arrivals, performances, red-carpet interviews and behind-the-scenes coverage across their websites and their Facebook and Instagram accounts through the night.</p>

<p>Coverage will include live reports from the festival&rsquo;s <b>VIP Creator Lounge</b>, produced by PR STARPOWER and styled by sponsor <b><a href="https://www.dollskill.com" rel="sponsored noopener" style="color:var(--signal)">Dolls Kill</a></b>, where a hand-picked group of creators will document the night for their own audiences.</p>

<p>SKVLK Fest was founded by <b>Anelise</b>, the daughter of Academy Award winner <b>Jamie Foxx</b>. The 2025 edition featured performances by <b>GloRilla</b>, <b>Tyga</b>, <b>Leon Thomas</b> and <b>YK Osiris</b>, according to published reports, and reached more than 100 million people, according to festival figures. Organizers say this year&rsquo;s edition is bigger.</p>

<p>Stories, photos and video from the festival will run on <a href="https://newswirehollywood.com" style="color:var(--signal)">newswirehollywood.com</a> and <a href="https://hollywoodnewsaccess.com" style="color:var(--signal)">hollywoodnewsaccess.com</a>, and will be available to partner outlets through the Newswire Hollywood wire.</p>

{GLANCE}
<h2>Media</h2>
<p>Journalists seeking interviews with SKVLK Fest&rsquo;s creators, producers and partners, or with questions about the festival, can contact PR STARPOWER at <a href="mailto:info@prstarpower.com?subject=SKVLK%20Fest%202026%20Media%20Request" style="color:var(--signal)">info@prstarpower.com</a>. See the <a href="pr-skvlk-fest-2026-media-advisory.html" style="color:var(--signal)">media advisory</a> for details.</p>

{ABOUT}"""
page("pr-skvlk-fest-2026-coverage.html",
     "Press Release: Newswire Hollywood and Hollywood News Access to Cover SKVLK Fest 2026 | Newswire Hollywood",
     hedA, re.sub("&rsquo;", "'", dekA), bodyA)

# ---------- RELEASE B: MEDIA ADVISORY ----------
hedB = "Media Advisory: Interviews With SKVLK Fest 2026 Creators, Producers and Partners Available Through PR STARPOWER"
dekB = "PR STARPOWER is fielding interview requests and press questions for Saturday&rsquo;s SKVLK Fest in Los Angeles, the youth-culture music and carnival festival sponsored in its VIP Creator Lounge by Dolls Kill."
bodyB = f"""<span class="prlabel">Press release &middot; Media advisory &middot; Issued by PR STARPOWER</span>
<div class="prmeta">FOR IMMEDIATE RELEASE &nbsp;&middot;&nbsp; Los Angeles &nbsp;&middot;&nbsp; Nov. 6, 2026</div>

<h1 style="margin-top:0">{hedB}</h1>

<p class="dek">{dekB}</p>

{FIG}{REEL}
<p><b>LOS ANGELES (Nov. 6, 2026) &mdash;</b> <b>PR STARPOWER</b>, which leads sponsorship, brand partnerships and publicity for <b>SKVLK Fest 2026</b>, is taking interview requests and press inquiries for the festival, which takes place Saturday, Nov. 7, in Los Angeles.</p>

<p>Reporters, producers and bookers who want to speak with the festival&rsquo;s creators, producers, sponsor or anyone connected to SKVLK Fest, or who have questions about coverage, should contact PR STARPOWER directly.</p>

<div class="card"><div class="card-head">Media advisory</div><div class="card-body"><dl class="qa">
<dt>What</dt><dd>SKVLK Fest 2026, a Los Angeles youth-culture music and carnival festival founded by Anelise, the daughter of Academy Award winner Jamie Foxx. Its 2025 edition drew 25,000 guests and turned away 15,000 more at capacity, according to the festival.</dd>
<dt>When</dt><dd>Saturday, Nov. 7, 2026</dd>
<dt>Where</dt><dd>Los Angeles. The festival is held at a private location; details go to approved media only.</dd>
<dt>Interviews</dt><dd>Requests for the festival&rsquo;s creators and producers, the PR STARPOWER lounge team, sponsor Dolls Kill and creators in the VIP Creator Lounge are coordinated by PR STARPOWER. Requests involving the Foxx family are passed along for consideration; availability is not guaranteed.</dd>
<dt>Visuals</dt><dd>Performances, a carnival setting, red-carpet arrivals and the Dolls Kill-styled VIP Creator Lounge.</dd>
<dt>Coverage on site</dt><dd>Newswire Hollywood, Hollywood News Access, and Billboard among other outlets</dd>
<dt>How to request</dt><dd>Email <a href="mailto:info@prstarpower.com?subject=SKVLK%20Fest%202026%20Interview%20Request" style="color:var(--signal)">info@prstarpower.com</a> with your name, outlet, role, the interview you want, your deadline and a link to recent work.</dd>
</dl></div></div>

<h2>Guidelines for media</h2>
<p>Many SKVLK Fest guests are under 18. Media may not photograph, film or interview minors without a parent&rsquo;s permission. Celebrity guests are filmed or interviewed only with the approval of their teams. The location is private and may not be published.</p>

<p>More: <a href="pr-skvlk-fest-2026-coverage.html" style="color:var(--signal)">Newswire Hollywood and Hollywood News Access to cover SKVLK Fest 2026</a> &middot; <a href="https://prstarpower.com/skvlk-fest.html" style="color:var(--signal)">PR STARPOWER: SKVLK Fest 2026</a></p>

{ABOUT}"""
page("pr-skvlk-fest-2026-media-advisory.html",
     "Media Advisory: SKVLK Fest 2026 Interviews Through PR STARPOWER | Newswire Hollywood",
     hedB, re.sub("&rsquo;", "'", dekB), bodyB)
print("built")
