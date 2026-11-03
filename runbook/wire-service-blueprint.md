# NEWSWIRE HOLLYWOOD WIRE — BLUEPRINT

What this is: the plan to build our own press release distribution and wire service. We use it for PR STARPOWER clients and sell it to others. It sits inside Newswire Hollywood as a separate division, kept apart from the newsroom. Researched 2026-11-03 at Terry's request. Status: PLAN. Nothing is built until Terry answers the decisions at the bottom.

## 1. What a wire service actually is (the reverse engineering)

Every big wire (PR Newswire/Cision, Business Wire, GlobeNewswire/Notified, EIN Presswire, ACCESS Newswire) is the same five layers:

| Layer | What it does | How the big wires do it |
|---|---|---|
| 1. Intake | Client submits; editors check facts, embargo, labels | Web form plus an editorial desk |
| 2. Newsroom feeds | Release lands inside newsroom and research systems | Contracts with AP, Dow Jones/Factiva, Bloomberg Terminal, LexisNexis, Moody's NewsEdge, Reuters |
| 3. Online syndication | Full text reposted on partner websites | Contracts with Yahoo Finance, Business Insider markets, Barchart, StreetInsider, FinancialContent (which powers many local TV and newspaper "markets" pages), Digital Journal, Benzinga |
| 4. Journalist outreach | Targeted emails to reporters by beat | Large licensed media databases |
| 5. The receipt | Report of every place the release appeared | Software searches the partner network for verbatim copies |

Scale, as the wires themselves claim it:
- Business Wire: 92,000+ outlets. Regional partners include Medianet (Australia), Korea Newswire, Nikkei and Jiji Press (Japan), PA Media and City A.M. (UK), The Canadian Press and Postmedia (Canada), DINO (Latin America, 500+ outlets).
- PR Newswire: 12,000+ websites and 550+ news content systems.
- EIN Presswire: AP News, Google News, Bloomberg Terminal, 100+ ABC, NBC, FOX, CBS and CW affiliate sites, plus about 3,900 "Affinity Group" sites. Those are owned by its own parent company (Newsmatics) and largely automated, not independent newsrooms.

## 2. The receipts: how to read them, and how we find them

PR Newswire's report searches its network for verbatim copies for 48 hours and reaches 98% completeness at 7 days. It lists "Exact Placements" by URL.

Public receipts are rare, but the placements are public web pages. The method:
1. Take a recent release from a given wire.
2. Search its exact headline in quotation marks.
3. Every site that reposted it shows up.

Do that across 20 releases per wire and you have that wire's real network map. An agent can do this legally, because it only reads public pages.

Several wires also publish their partner lists openly: InvestorWire and NetworkWire "Syndication Partners" pages, EMWNews "distribution partners", ACCESS Newswire "top pickup sites".

## 3. Can we do the same? Yes, in three phases

PHASE 1: launch fast, with global reach from day one
- Sign up as a white-label reseller with an established wire. Our brand, our price, their network, and their receipt carrying our logo.
- Programs found (vendor claims; verify before paying): PRNow (reseller about $11 a release), Press Ranger (wholesale $299 to $399), 24presse (about €119 wholesale against €395 retail), RedPress (claims AP, Yahoo Finance, MarketWatch), NewswireNEXT ($299, white label by default).
- Test two of them with one real release each. Compare the receipts. Keep the better one.
- At the same time, every release also runs on our own network: four sites, news feeds, Google News, Apple News, the social blast.

PHASE 2: build our own direct partnerships (months)
- Partner outreach to the syndication receivers: FinancialContent, Digital Journal, Benzinga, MENAFN, regional wires abroad.
- Apply as a content provider to LexisNexis and Factiva.
- Every agreement goes in a tracker. Terry signs. An agent drafts and follows up.

PHASE 3: our own receipt engine
- After each release, an agent searches the known partner sites for the headline and builds a branded pickup report for the client.
- This costs almost nothing to run on GitHub Actions.

Video: the same model. Host on our page and YouTube, then push to every platform through the social scheduler (see mass-distribution-plan.md).

## 4. Honest limits

- AP, Yahoo Finance and Bloomberg do not take feeds from a brand-new wire. They want volume, compliance and a track record. The reseller phase bridges that gap.
- Journalist contacts: publicly listed newsroom desks and press inboxes are fine to approach. Mass cold email to personal addresses risks US anti-spam law (CAN-SPAM: honest sender, physical address, working opt-out) and EU privacy law (GDPR). It also gets our domain blacklisted. Build an opt-in "subscribe to the wire" list, and send targeted pitches from the private Rolodex.
- Do not copy the "thousands of automated sites" model. Google penalizes mass auto-generated sites, and journalists don't read them.
- Rankings: links inside paid releases must carry rel="sponsored" or rel="nofollow". A wire's value is discovery, not links. Our own articles are what rank.
- Paid releases carry a visible label and live in a separate wire section, never mixed in with newsroom stories.

## 5. How many agents? Four, running in parallel

1. Intake and compliance: checks the release, embargo, labels, image rights.
2. Distribution: publishes to our sites and feeds, sends to the reseller, writes the social posts.
3. Receipt tracker: finds pickups and builds the client report.
4. Partner outreach: researches partners and drafts partnership emails for Terry to approve.

No new website is needed yet. wire.newswirehollywood.com is a free subdomain of the domain we already own.

## 6. Decisions needed from Terry

1. Brand name, e.g. "Newswire Hollywood Wire" or "Hollywood Wire".
2. Free subdomain now, or buy a separate domain.
3. Approve testing two resellers with one release each (about $300 to $700 total, to be confirmed).
4. Which release is the first test.
5. Client terms of service and refund policy: have a licensed attorney review them before we sell.
