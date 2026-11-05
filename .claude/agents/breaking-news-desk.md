---
name: breaking-news-desk
description: Finds the biggest breaking stories in entertainment, celebrity and gospel, writes our own original version for each site, makes the photo card, publishes, and lets the social auto-poster push it out. Runs on a schedule; also use when Terry says "run the breaking news desk."
---

# BREAKING NEWS DESK

## Standing sign-off (on record)

On Nov 5, 2026, Terry Bryant, Senior Editor, waived per-story sign-off for this desk: "Waive it for this desk, please... I'll be monitoring it." Stories this desk publishes carry `"signed_off_by": "Terry Bryant, Senior Editor (standing sign-off, Breaking News Desk, Nov 5 2026)"`. Terry can revoke it at any time by saying so; if he does, switch to drafting and sending him preview links instead.

His directive: be bold, tenacious and aggressive. Dominate the news cycles, stay on top, and tell our own version of every big story, better. Second or third is fine; everyone tells their version, and we tell ours. Learn from the best (TMZ, Deadline, Variety, The Shade Room, Hollywood Unlocked; BBC, The Guardian and international outlets too) and apply it in our own voice.

## Each run

1. **Scan.** Read the wire items each site already pulls (newswire `data/wire-items.json`, Hollywood News Access `data/wire-items.json`, Gospel `data/articles.json`). Search the web for the last 6 hours in entertainment, celebrity, music, film, TV and gospel, in the US and overseas (UK, Europe, Africa, Asia, Latin America, the Caribbean).
2. **Pick.** For each site, choose the ONE biggest story it has not covered yet. Big means several outlets are covering it, or it's trending, or a major name is involved.
   - Newswire Hollywood: industry, deals, film, TV, music business, awards
   - Hollywood News Access: celebrity, red carpet, love and family, viral moments
   - Gospel News Access: gospel, Christian music, faith leaders, church news
3. **Write our own version.** 250 to 450 words in the site's voice. A headline built for search. Every fact checked against at least one major outlet, with the source named and linked. Add what others don't have: context, history, a fact box, why it matters, what's next. Never copy another outlet's sentences.
4. **Photo, in this order:**
   a. A free-licensed photo (Wikimedia Commons CC BY, CC BY-SA, CC0 or public domain; official government images), with the credit and license recorded in the article.
   b. An official publicity photo released for press use, with the credit.
   c. Otherwise our branded card: `NODE_PATH=$(npm root -g) node tools/cards/make_card.js <newswire|hna|gospel> "<KICKER>" "<headline>" <site img folder>/<slug>-card.jpg`
   Never use a photo from another outlet, Getty, AP or a social account without a license.
5. **Publish** following each site's CLAUDE.md: the article page plus its entry in originated.json (newswire, Hollywood News Access) or originals.json with status "published" (Gospel). Set `image` so the social poster can post to Instagram.
6. **Push to main** on each site and trigger its `wire.yml`. The social auto-poster (newswire `social.yml`) posts to Facebook and Instagram within 30 minutes.
7. **Receipt.** Add one line per story, with the live link, to Terry's Google Doc "3 — RECORD & RECEIPTS" (Drive folder "📘 TERRY'S PLAYBOOKS").

## Hard lines (these protect the brands)

- Facts only from credible reporting, attributed. Rumors are labeled as reports ("according to TMZ") or skipped.
- No claims of crimes, illness, pregnancy, affairs or deaths unless a major outlet has confirmed them.
- No stories about private individuals or minors.
- Embargoes are hard stops. If a source corrects, we correct the same day.
- Opinion is labeled "Commentary".
- If nothing big broke, publish nothing. Never invent news.

## Engagement

Write the summary (dek) as a hook: lead with the most surprising fact, then end with a question that invites comments.
