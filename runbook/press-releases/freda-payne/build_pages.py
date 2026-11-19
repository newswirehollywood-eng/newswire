#!/usr/bin/env python3
"""Builds the two Newswire Hollywood pages for Freda Payne / Motown for Veterans
(Nov 19, 2026) from the house press-release template. Run once; pages are then hand-owned."""
import json, os, re, html
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
T = open(os.path.join(R, "docs/pr-skvlk-fest-2026-community-thanks.html"), encoding="utf-8").read()
head_css = T[T.index("<style>"):T.index("</style>") + 8]
follow = T[T.index("<!-- FOLLOW:START -->"):T.index("<!-- FOLLOW:END -->") + 19]
SITE = "https://newswirehollywood.com/"
TIX = "https://www.ticketmaster.com/motown-for-veterans-benefit-concert-tempe-arizona-01-08-2027/event/19006522B3C069C6"
VENUE = "https://mullettarena.com/event/motown/"
AMZ = "https://www.amazon.com/s?k=Freda+Payne"

def page(fn, title, ogtitle, desc, img, label, prmeta, h1, body, footer_links, kind):
    ld = {"@context": "https://schema.org", "@type": "NewsArticle", "headline": ogtitle,
          "datePublished": "2026-11-19", "image": [SITE + img],
          "author": {"@type": "Organization", "name": "PR STARPOWER" if kind == "pr" else "Newswire Hollywood"},
          "publisher": {"@type": "Organization", "name": "Newswire Hollywood", "url": "https://newswirehollywood.com"},
          "about": {"@type": "MusicEvent", "name": "Motown for Veterans Benefit Concert",
                    "startDate": "2027-01-08T19:00:00-07:00", "doorTime": "2027-01-08T18:00:00-07:00",
                    "eventStatus": "https://schema.org/EventScheduled",
                    "location": {"@type": "Place", "name": "Mullett Arena", "address": "411 S. Packard Dr., Tempe, AZ 85281"},
                    "performer": [{"@type": "Person", "name": "Freda Payne"},
                                  {"@type": "MusicGroup", "name": "The Former Ladies of the Supremes"},
                                  {"@type": "MusicGroup", "name": "Glenn Leonard's Temptations Revue"},
                                  {"@type": "MusicGroup", "name": "Jr. Walker's All-Star Band"},
                                  {"@type": "Person", "name": "Alli Starr"}],
                    "offers": {"@type": "Offer", "url": TIX, "lowPrice": "89", "highPrice": "235", "priceCurrency": "USD"}}}
    e = html.escape
    out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="index,follow,max-image-preview:large">
<title>{e(title)} | Newswire Hollywood</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(ogtitle)}">
<meta property="og:type" content="article">
<link rel="canonical" href="{SITE}{fn}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Narrow:wght@500;600;700&family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&display=swap" rel="stylesheet">
{head_css}
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
<!-- SOCIAL -->
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{fn}">
<meta property="og:image" content="{SITE}{img}">
<meta property="og:site_name" content="Newswire Hollywood">
<meta property="article:published_time" content="2026-11-19">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(ogtitle)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}{img}">
<!-- /SOCIAL -->
</head>
<body>

<header class="masthead"><div class="wrap">
<a class="brand" href="index.html">Newswire <em>Hollywood</em></a>
<div class="standfirst">The business behind the business</div>
<div class="dateline">Los Angeles, California &middot; Thursday, November 19, 2026</div>
</div></header>

<nav class="nav"><ul>
<li><a href="index.html">Home</a></li>
<li><a href="film.html">Film</a></li>
<li><a href="television.html">Television</a></li>
<li><a href="music.html">Music</a></li>
<li><a href="fashion.html">Fashion</a></li>
<li><a href="deals.html">Deals</a></li>
<li><a href="ai-tech.html">AI &amp; Big Tech</a></li>
<li><a href="calendar.html">The Calendar</a></li>
<li><a href="pressroom.html">Press Room</a></li>
</ul></nav>

<main>
<article class="art">
<span class="prlabel">{label}</span>
<div class="prmeta">{prmeta}</div>

<h1 style="margin-top:0">{h1}</h1>
{body}
</article>
</main>

{follow}
<footer><div class="wrap">
<nav>
<a href="index.html">Home</a>
<a href="music.html">Music</a>
<a href="pressroom.html">Press Room</a>
{footer_links}
</nav>
<div>&copy; 2026 Newswire Hollywood. Los Angeles, California.</div>
</div></footer>

</body>
</html>
"""
    open(os.path.join(R, "docs", fn), "w", encoding="utf-8").write(out)

A = 'style="color:var(--signal)"'
FACTS = f"""<div class="card"><div class="card-head">The event</div><div class="card-body"><dl>
<dt>What</dt><dd>Motown for Veterans Benefit Concert</dd>
<dt>When</dt><dd>Friday, Jan. 8, 2027. Doors 6 p.m., show 7 p.m. (Arizona time)</dd>
<dt>Where</dt><dd>Mullett Arena, 411 S. Packard Dr., Tempe, Ariz.</dd>
<dt>On the bill</dt><dd>The Former Ladies of the Supremes, Glenn Leonard&rsquo;s Temptations Revue, Jr. Walker&rsquo;s All-Star Band, Freda Payne and Alli Starr</dd>
<dt>Benefits</dt><dd>Green Homes for Vets, a 501(c)(3) building an eco-friendly home community for returning combat service men and women in Prescott Valley, Ariz.</dd>
<dt>Tickets</dt><dd><a href="{TIX}" {A} rel="noopener">Ticketmaster</a>, $89 to $235 as listed. Premium suites and loge upgrades through the <a href="{VENUE}" {A} rel="noopener">Mullett Arena event page</a>.</dd>
</dl></div></div>"""

# ---------- 1. PR STARPOWER press release ----------
pr_body = f"""
<p class="dek">The &ldquo;Band of Gold&rdquo; singer joins the Former Ladies of the Supremes, Glenn Leonard&rsquo;s Temptations Revue and Jr. Walker&rsquo;s All-Star Band on Jan. 8 at Mullett Arena in Tempe, Ariz. Proceeds go to Green Homes for Vets.</p>

<figure class="pr-img">
  <img src="img/freda-payne-2026/freda-payne-portrait-white.jpg" alt="Freda Payne laughing, in a white one-shoulder top and gold earrings, against a pale background">
  <figcaption>Freda Payne. Photo courtesy of Freda Payne / PR STARPOWER. Available for editorial use with credit.</figcaption>
</figure>

<p><b>LOS ANGELES (Nov. 19, 2026) &mdash;</b> Freda Payne, the Detroit-born singer whose &ldquo;Band of Gold&rdquo; became a worldwide hit in 1970, will perform at the Motown for Veterans Benefit Concert on Friday, Jan. 8, 2027, at Mullett Arena in Tempe, Ariz., PR STARPOWER announced today.</p>

<p>Payne shares the bill with the Former Ladies of the Supremes, Glenn Leonard&rsquo;s Temptations Revue, Jr. Walker&rsquo;s All-Star Band and Alli Starr. Doors open at 6 p.m. and the show begins at 7 p.m.</p>

<p>Proceeds benefit Green Homes for Vets, a 501(c)(3) organization working to build an eco-friendly home community in Prescott Valley, Ariz., for combat service men and women returning home.</p>

<p>Tickets are on sale now through <a href="{TIX}" {A} rel="noopener">Ticketmaster</a>, listed from $89 to $235. Premium suites and loge upgrades are available, along with VIP meet-and-greet and sponsorship packages and an online silent auction, according to the event&rsquo;s listings. Details: <a href="{VENUE}" {A} rel="noopener">mullettarena.com/event/motown</a>.</p>

<h2>A legend&rsquo;s season</h2>

<p>The Tempe date caps a busy fall for Payne, 84. On Sept. 26 she played to a sold-out Catalina Jazz Club in Los Angeles with <i>Freda Payne Portrays and Honors Legendary Ladies of Song</i>, written and directed by Donald B. Welch, a night Newswire Hollywood&rsquo;s review called &ldquo;not a tribute show&rdquo; but &ldquo;testimony.&rdquo; In late October she performed at sea aboard Holland America, on a Fort Lauderdale-to-Puerto Rico sailing that also featured Darlene Love and Wayne Newton.</p>

<figure class="pr-img">
  <img src="img/freda-payne-2026/freda-payne-pink-gown.jpg" alt="Freda Payne in a beaded blush gown, standing in an open doorway and looking up">
  <figcaption>Freda Payne. Photo courtesy of Freda Payne / PR STARPOWER. Available for editorial use with credit.</figcaption>
</figure>

{FACTS}

<h2>Media</h2>

<p>High-resolution photographs are available for editorial use with credit &ldquo;Courtesy of Freda Payne / PR STARPOWER.&rdquo; Interview requests for Freda Payne go to PR STARPOWER.</p>

<h2>About Freda Payne</h2>

<p>Freda Payne is a singer and actress from Detroit whose career spans six decades. Her 1970 single &ldquo;Band of Gold&rdquo; became an international hit, and she followed it with &ldquo;Bring the Boys Home,&rdquo; her 1971 anti-war song of the Vietnam era. A two-time Grammy nominee, she has worked across jazz, pop, R&amp;B and the stage. Her memoir, <i>Band of Gold: A Memoir</i>, is available now. Official website: <a href="https://www.fredapayne.net/" {A} rel="noopener">fredapayne.net</a>.</p>

<h2>About PR STARPOWER</h2>

<p>PR STARPOWER is a Los Angeles publicity and public relations company representing artists, productions and events in entertainment, music and culture. It represents Freda Payne. <a href="https://prstarpower.com" {A}>prstarpower.com</a></p>

<div class="ends">###</div>

<div class="contact">
  <p style="margin-bottom:10px"><b>MEDIA CONTACT</b></p>
  <p style="margin-bottom:4px">PR STARPOWER Media Relations &middot; Terry Bryant</p>
  <p style="margin-bottom:0"><a href="mailto:info@prstarpower.com?subject=Freda%20Payne%20%2F%20Motown%20for%20Veterans" {A}>info@prstarpower.com</a> &middot; 646-315-2942</p>
</div>

<p style="font-family:var(--hed);font-size:13px;color:#7A7A7A;border-top:1px solid var(--rule);padding-top:16px">Disclosure: this release is issued by PR STARPOWER, which represents Freda Payne. PR STARPOWER and Newswire Hollywood are sister companies. Event details are from the Mullett Arena and Ticketmaster listings; PR STARPOWER is not the event&rsquo;s presenter.</p>

<p><a href="freda-payne-motown-for-veterans-tempe.html" {A}><b>Newswire Hollywood&rsquo;s story &rsaquo;</b></a> &nbsp;&middot;&nbsp; <a href="freda-presskit.html" {A}><b>Press kit &rsaquo;</b></a> &nbsp;&middot;&nbsp; <a href="pressroom.html" {A}><b>Press Room &rsaquo;</b></a></p>
"""
page("pr-freda-payne-motown-for-veterans.html",
     "Press Release: Freda Payne to Perform at Motown for Veterans Benefit Concert Jan. 8 in Tempe",
     "Freda Payne to Perform at Motown for Veterans Benefit Concert Jan. 8 in Tempe, Ariz.",
     "The “Band of Gold” singer joins the Former Ladies of the Supremes, Glenn Leonard’s Temptations Revue and Jr. Walker’s All-Star Band at Mullett Arena. Proceeds benefit Green Homes for Vets.",
     "img/freda-motown-veterans-share-prs.jpg",
     "Press release &middot; Issued by PR STARPOWER on behalf of Freda Payne",
     "FOR IMMEDIATE RELEASE &nbsp;&middot;&nbsp; Los Angeles &nbsp;&middot;&nbsp; Nov. 19, 2026",
     "Freda Payne to Perform at Motown for Veterans Benefit Concert Jan. 8 in Tempe, Ariz.",
     pr_body, '<a href="freda-payne-motown-for-veterans-tempe.html">Freda Payne sings for veterans</a>', "pr")

# ---------- 2. Newswire Hollywood announcement story ----------
nw_body = f"""
<p class="dek">Fifty-five years after &ldquo;Bring the Boys Home,&rdquo; the &ldquo;Band of Gold&rdquo; legend heads to Tempe to sing for veterans on a bill with the Former Ladies of the Supremes and the Temptations Revue.</p>

<div class="byline">By the <b>Music Desk</b>, Newswire Hollywood &middot; Nov. 19, 2026</div>

<figure class="pr-img">
  <img src="img/freda-payne-2026/freda-payne-portrait-white.jpg" alt="Freda Payne laughing, in a white one-shoulder top and gold earrings, against a pale background">
  <figcaption>Freda Payne. Photo courtesy of Freda Payne / PR STARPOWER.</figcaption>
</figure>

<p><b>LOS ANGELES &mdash;</b> In 1971, Freda Payne sang &ldquo;Bring the Boys Home,&rdquo; a Vietnam-era plea to bring American soldiers home from the war. On Jan. 8, the &ldquo;Band of Gold&rdquo; singer sings for the veterans who made it back.</p>

<p>Payne, 84, is on the bill for the <b>Motown for Veterans Benefit Concert</b> at Mullett Arena in Tempe, Ariz., alongside the Former Ladies of the Supremes, Glenn Leonard&rsquo;s Temptations Revue, Jr. Walker&rsquo;s All-Star Band and Alli Starr. Doors open at 6 p.m.; the music starts at 7.</p>

<p>The money goes to <b>Green Homes for Vets</b>, a 501(c)(3) building an eco-friendly home community in Prescott Valley, Ariz., for combat service men and women returning from duty, according to the arena&rsquo;s listing.</p>

<h2>Detroit, by way of everywhere</h2>

<p>The Motown banner fits the Detroit sound Payne grew up in, even though her biggest hits came out on Invictus, the label Holland-Dozier-Holland founded after leaving Motown. &ldquo;Band of Gold&rdquo; went to No. 1 in the United Kingdom in 1970 and made her a name worldwide.</p>

<p>She arrives in Tempe off a strong fall. In September she sold out Catalina Jazz Club in Hollywood with <i>Legendary Ladies of Song</i>, a night <a href="freda-payne-catalina-legendary-ladies-review.html" {A}>this desk reviewed</a> as &ldquo;not a tribute show&rdquo; but &ldquo;testimony.&rdquo; In late October she performed at sea on a Holland America sailing with Darlene Love and Wayne Newton.</p>

<figure class="pr-img">
  <img src="img/freda-payne-2026/freda-payne-pink-gown.jpg" alt="Freda Payne in a beaded blush gown, standing in an open doorway and looking up">
  <figcaption>Freda Payne. Photo courtesy of Freda Payne / PR STARPOWER.</figcaption>
</figure>

<h2>Getting in</h2>

<p>Tickets are on Ticketmaster, listed from $89 to $235, with premium suites, loge upgrades, VIP meet-and-greet packages and an online silent auction also offered.</p>

<p style="margin:26px 0"><a href="{TIX}" rel="noopener" style="display:inline-block;background:var(--signal);color:#fff;font-family:var(--hed);font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:14px;padding:13px 22px;border-radius:3px">Get tickets on Ticketmaster &rsaquo;</a></p>

{FACTS}

<p style="font-size:16px">Listen: <a href="{AMZ}" {A} rel="noopener">Freda Payne on Amazon</a>, including &ldquo;Band of Gold&rdquo; and her memoir, <i>Band of Gold: A Memoir</i>.</p>

<p style="font-family:var(--hed);font-size:13px;color:#7A7A7A;border-top:1px solid var(--rule);padding-top:16px">Disclosure: Freda Payne is a client of PR STARPOWER, Newswire Hollywood&rsquo;s sister company. PR STARPOWER&rsquo;s <a href="pr-freda-payne-motown-for-veterans.html" {A}>press release is here</a>. Event details are from the Mullett Arena and Ticketmaster listings. Newswire Hollywood may earn a commission from some links.</p>
"""
page("freda-payne-motown-for-veterans-tempe.html",
     "Freda Payne Sings for Veterans at Motown Benefit Concert in Tempe Jan. 8",
     "Freda Payne Sings for Veterans at Motown Benefit Concert in Tempe Jan. 8",
     "Fifty-five years after “Bring the Boys Home,” the “Band of Gold” legend joins the Former Ladies of the Supremes and the Temptations Revue at Mullett Arena to benefit Green Homes for Vets.",
     "img/freda-motown-veterans-share-nwh.jpg",
     "Music &middot; Client news, disclosed below",
     "TEMPE, ARIZ. &nbsp;&middot;&nbsp; JAN. 8, 2027 &nbsp;&middot;&nbsp; MULLETT ARENA",
     "Freda Payne Sings for Veterans at Motown Benefit Concert in Tempe Jan. 8",
     nw_body, '<a href="pr-freda-payne-motown-for-veterans.html">Press release</a>', "story")
print("built")
