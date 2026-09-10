# PUNCH LIST

Running list of what is built, what is next, and what needs a decision from Terry.

## BUILT

Repo, standing rules in CLAUDE.md, folder structure
Events Calendar agent — real, loadable by Claude Code at .claude/agents/events-calendar-agent.md
Rapid Response Desk agent (doc only — not yet made real like the Events Calendar agent)
Live homepage on GitHub Pages — was rendering blank white from a truncated file, fixed 2026-09-09
NewsArticle / NewsMediaOrganization / CollectionPage schema on every live page
Email alias naming decided (see runbook/services.md) — not active until Terry sets up the mailbox backend

## NEXT — SEO MACHINERY

News sitemap, auto-generated, 48-hour window only
Standard XML sitemap
robots.txt
Article template with NewsArticle schema
IndexNow ping on publish
Google Search Console verification

## NEXT — PAGES

The Calendar, public facing
Press Room: media kit, rate card, credentialing, wire submission
Social page with live feeds
The Wire: syndicated and sponsored, tagged

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

## PRODUCT LINE

Package the full system as a licensable newsroom operating system.
Branding isolated to one config file so it swaps per client.
