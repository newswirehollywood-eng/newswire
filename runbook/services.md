# SERVICES AND ACCOUNTS

Every third party this operation touches. What it does, what it costs, what it is for, and status.
Update this file whenever an account is created or changed.

## LIVE NOW

GITHUB
Account: newswirehollywood-eng
Repo: github.com/newswirehollywood-eng/newswire
Purpose: everything lives here. Files, agents, automation.
Cost: free. Public repo means unlimited Actions minutes.
Note: a second account exists, mainsource, unused. Ignore it.

GITHUB PAGES
Live at: newswirehollywood-eng.github.io/newswire/
Purpose: hosts the site. Serves from the docs folder on the main branch.
Cost: free.
Settings: github.com/newswirehollywood-eng/newswire/settings/pages

GOOGLE FONTS
Purpose: Archivo Narrow and Newsreader, loaded on every page.
Cost: free. No account needed.

## NEEDED NEXT

DOMAIN REGISTRAR
Status: LIVE. newswirehollywood.com is purchased and pointed at GitHub Pages — confirmed working via docs/CNAME and a real GitHub Pages deployment. Not a blocker anymore.

FORMSPREE
Where: formspree.io
Purpose: receives Press Room form submissions and emails them to Terry.
Cost: free tier, 50 submissions a month. Paid tiers above that.
Status: needs signup. The form endpoint ID goes into docs/pressroom.html.

GOOGLE SEARCH CONSOLE
Where: search.google.com/search-console
Purpose: proves site ownership to Google, submits sitemaps, reports indexing.
Cost: free.
Status: needed before SEO machinery pays off.

## PAYMENTS, FOR PRESS RELEASE REVENUE

STRIPE OR PAYPAL
Purpose: collecting press release distribution and advertising payments.
Cost: roughly 2.9 percent plus 30 cents per transaction.
Status: not set up. Needed before the first paid release.

## EMAIL AND NEWSLETTER

Options: Beehiiv, Substack, Buttondown, MailerLite.
Purpose: the industry brief newsletter. This is the highest-value revenue line we can build.
Cost: free tiers exist at small list sizes on most.
Status: not chosen. Needs a decision.

BUSINESS EMAIL
Purpose: a real address on our own domain, not a personal one. Credentialing desks check this.
Backend: confirmed 2026-09-11 — info@newswirehollywood.com already exists, GoDaddy-hosted, running on Microsoft 365/Outlook. Not Gmail, not Zoho — the earlier free-path research assumed no mailbox existed yet; corrected now that it does. Already-paid-for, so Microsoft Graph API access for the triage agent rides on that existing subscription at no new cost.
Status: mailbox is live. Aliases are decided (below), not yet created in the Microsoft 365 admin center as of 2026-09-11.

ALIASES — confirmed 2026-09-09, naming is settled, Terry activates them once the mailbox backend is chosen
Already promised publicly on docs/pressroom.html, so these five must exist exactly as named:
  news@newswirehollywood.com — news desk, general editorial tips
  calendar@newswirehollywood.com — calendar listings
  wire@newswirehollywood.com — press releases and wire submissions
  advertising@newswirehollywood.com — advertising and partnerships
  corrections@newswirehollywood.com — corrections
Recommended additions, not yet promised anywhere so lower priority:
  tips@newswirehollywood.com — a dedicated confidential tip line reads differently to a source than a general news@ address, and Rule 25 (contact discipline) calls out tip lines specifically
  hello@newswirehollywood.com — catch-all for anything that doesn't fit the others
All of these can forward to one real inbox Terry checks — they don't need separate mailboxes, just routing rules — so the naming decision doesn't depend on which backend (Zoho vs. Cloudflare+Gmail) gets picked.

## MONITORING AND RESEARCH, FREE

Google Trends, Reddit public feeds, YouTube, Bluesky open API, trade and wire RSS.
Cost: free. No accounts required.

## MONITORING, PAID, LATER

Instagram and TikTok native monitoring requires a paid provider or an official business API connection. Both platforms closed public data access.
Status: deferred. Cross-platform spillover covers most stories for now.

## IMAGES

Studio and label press assets, supplied with permission: free.
Original photography: free once we have a credentialed shooter.
Wire licensing, Getty or AP: paid, and expensive.
Rule: never unlicensed. Every image records its source.

## COST SUMMARY

Running today: zero.
To be fully operational: the domain, roughly 12 dollars a year, and payment processing fees only when we get paid.
Everything else stays on free tiers until volume requires otherwise.
