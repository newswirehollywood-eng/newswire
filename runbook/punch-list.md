# PUNCH LIST

Running list of what is built, what is next, and what needs a decision from Terry.

## BUILT

Repo, standing rules in CLAUDE.md, folder structure
Events Calendar agent — real, loadable by Claude Code at .claude/agents/events-calendar-agent.md, ran its first real sweep 2026-09-11 (14 events, 14 contacts, confidence marked honestly)
Trend Watch agent — real, ran twice (2026-09-10, 2026-09-11), output in pulse/trend-watch-brief.md
Email Triage agent — real definition at .claude/agents/email-triage-agent.md, blocked on Graph API setup (see below — also see the Gmail note)
Rapid Response Desk agent (doc only — not yet made real like the above three)
Live homepage on GitHub Pages — was rendering blank white from a truncated file, fixed 2026-09-09
NewsArticle / NewsMediaOrganization / CollectionPage schema on every live page
Email alias naming decided (see runbook/services.md) — not active until Terry sets up the mailbox backend
Real desk-byline system live everywhere (style/house-style.md, data/masthead.json) — never-invent-a-person rule enforced
5 real published articles: Emmys 2026, Freda Payne/Catalina, TIFF 2026, the Sony/Warner-Anthropic lawsuit, the IMAX box office record

BUILT 2026-09-15, full SEO/pages pass:
News sitemap fixed — was carrying stale entries older than 48 hours (a real bug, now corrected), auto-regenerates daily via .github/workflows/news-sitemap.yml, dry-run tested against the real repo before being trusted
Standard sitemap.xml — every real page now listed with accurate lastmod dates
robots.txt — already referenced both sitemaps correctly, no change needed
docs/_template-article.html — commented placeholder template for the next new article
9 section pages built: film.html, television.html, music.html, fashion.html, sports.html, deals.html, ai-tech.html, international.html, wire.html — same masthead/nav/footer as home, real links to existing coverage where it exists, honest "coverage begins" notes where it doesn't (sports and international currently have zero real content — sports is a new category this pass introduced that was never part of the original vertical list; flagging that as a real question for Terry, not assuming it belongs)
Nav on every page (including the 8 pre-existing ones) now points to real section URLs instead of index.html anchors
Wire separation: wire.html carries syndicated/sponsored only, tagged, currently empty (nothing has run through either intake path yet), excluded from news-sitemap by construction
Weekly link-check workflow (.github/workflows/link-check.yml) — dry-run tested against the real repo, logs to runbook/errors.md, does not check external links (would need network calls out of scope for this pass)
IndexNow ping on publish and Google Search Console verification — still not done, see the list below

## DISCOVERED THIS PASS, NOT YET ACTED ON

Gmail, Google Calendar, and Google Drive tools are now connected to this session (appeared 2026-09-15). This may replace the GoDaddy/Microsoft Graph API plan discussed 2026-09-11 for the Email Triage agent — worth confirming with Terry which mailbox is actually meant to be the real one before building further, rather than assuming.

## NEXT — REVENUE

Newsletter signup on every page, list building starts immediately
Rate card built on real comparables
AI and Big Tech vertical priced as tech inventory, not entertainment
Sponsored content template, native format
Ad network application once traffic qualifies

## NEXT — AGENTS

Story Scout
Assignment Desk
Writer
Copy Desk
Headline and SEO
Photo and Assets
Publishing
Distribution
Analytics
Publicity division, five agents
Revenue division, four agents
Industry and Tech Pulse, four agents

## WHEN TERRY'S BACK — the whole current list in one place, so nothing has to be held in his head

Read top to bottom, each is quick, none require research first:

1. **Send the two photo permission emails.** Drafted and ready in `runbook/photo-sourcing.md` — one for the Emmys 2026 Television Academy contact, one for Catalina Jazz Club. Has to come from Terry's own address or it reads as fake. Not sent as of 2026-09-10.
2. **Fill in the social media table.** `runbook/social-media-plan.md` has a blank table (platform / handle / who owns the login / active or dormant) for whatever Newswire Hollywood accounts already exist. Nothing else on social can move until this is filled in.
3. **Google Search Console.** Terry said he'd get the verification code himself (meta tag, not an HTML file) and paste it back — still pending as of 2026-09-10.
4. **Confirm the exact masthead title wording.** Everything else about the desk/byline system is built and live; this one field in `data/masthead.json` is the only thing waiting on Terry.
5. **Email setup, two browser-only steps** (`.claude/agents/email-triage-agent.md` has the details): Cloudflare Email Routing forwarding news@ into a real Gmail inbox, then a Google Cloud OAuth credential for that inbox. Offered to walk through both live, screen by screen, whenever Terry's ready.
6. **Affiliate distribution channel names** — real names only, can't be researched or guessed.

Lower priority, no rush: Formspree signup (pending, not blocking), newsletter platform choice (on hold per Terry's own instruction, do not build until told).

Note on the 2026-09-15 build order: it listed "domain name and registrar" as still blocked on Terry. That's stale — the domain has been live since 2026-09-07 (see runbook/services.md). Not re-blocking on something already resolved.

New from this pass: decide whether "Sports" is a real vertical for Newswire Hollywood or should be cut — it was added to the section-page list this pass without being part of the original coverage plan, and has zero content behind it right now.

## PRODUCT LINE

Package the full system as a licensable newsroom operating system.
Branding isolated to one config file so it swaps per client.
