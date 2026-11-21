# Technical Stack for Fast News Indexing (Top Stories / Discover / Google News) — and How a Static GitHub Pages Site Matches It

Research date: 2026-11-21. Method note: in this cloud session, direct page fetches of developers.google.com and indexnow.org were blocked by the network allowlist, so the Google and IndexNow findings below come from search-engine extracts of those official pages (URLs cited are the official pages the extracts quote). Where only secondary sources were available, that is said. Items marked "repo check" come from reading this repository's own files on 2026-11-21, not from the web.

---

## 1. Discovery and crawl signals: news sitemaps, ping, RSS/WebSub, Indexing API, IndexNow

### Takeaway
For Google, the only official fast-discovery levers left are an accurate, constantly-updated news sitemap (plus normal sitemap/RSS with honest `lastmod`), a crawlable homepage/section pages that link to new stories, and Search Console — sitemap "ping" is dead (2023) and the Indexing API is officially restricted to JobPosting/livestream pages. For Bing, Yandex, Naver, Seznam (and, via Bing, ChatGPT search), IndexNow is the instant-notification standard and the official replacement for Bing's sitemap ping and PubHub.

### Cited Findings
**News sitemaps (Google rules)**
- Only list articles created in the last two days; remove older entries or strip their `<news:news>` metadata. — [Google Search Central: News sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en); [Google News Publisher Help: News sitemaps](https://support.google.com/news/publisher/answer/74288)
- Up to 1,000 `<news:news>` tags per sitemap; each `<url>` may carry only one `<news:news>`; above 1,000, split into several sitemaps (sitemap index). — [Google Search Central: News sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en)
- `<news:name>` must exactly match the publication name as shown on news.google.com (text in parentheses ignored). `<news:language>` is an ISO 639 2–3 letter code (exceptions: `zh-cn`, `zh-tw`). — [Google Search Central: News sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en)
- Secondary guidance: update the existing news sitemap rather than create a new one per article; keep it limited to recently published stories. — [Sitebulb: Ink to Code, technical SEO for news publishers](https://sitebulb.com/resources/guides/ink-to-code-technical-seo-considerations-for-news-publishers); [Lumar: SEO for news publisher websites](https://www.lumar.io/blog/best-practice/seo-for-news-publisher-websites)

**Sitemap ping — DEPRECATED**
- Google announced on 26 June 2023 that the sitemaps ping endpoint would stop working in ~6 months; calls now return 404 and accomplish nothing (existing code calling it "won't break Search"). Submit sitemaps via robots.txt and Search Console instead. — [Google Search Central Blog, June 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping); [Search Engine Land](https://searchengineland.com/google-to-deprecate-sitemaps-ping-endpoint-later-this-year-428661); [Search Engine Roundtable](https://www.seroundtable.com/google-to-drop-support-for-sitemaps-ping-endpoints-35617.html)
- Google's replacement advice: keep `lastmod` accurate; `lastmod` should reflect substantive changes, not sidebar/footer edits, and Google stops trusting `lastmod` on sites whose dates don't match reality. — [Google Search Central Blog, June 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)
- Frameworks removed their ping helpers as a result (e.g., Django `ping_google()`). — [Django ticket #34688](https://code.djangoproject.com/ticket/34688)
- Bing's sitemap ping endpoint also stopped working; Bing says send updated URLs directly via IndexNow. — [ctrl.blog: Bing stops accepting sitemap pings](https://www.ctrl.blog/entry/sitemap-ping-indexnow/)

**Google Indexing API — NOT for news**
- Officially usable only for pages with `JobPosting` or `BroadcastEvent` embedded in a `VideoObject` (livestreams). — [Google: Using the Indexing API](https://developers.google.com/search/apis/indexing-api/v3/using-api)
- Default quota: 200 publish requests/day per project (URL_UPDATED + URL_DELETED), resetting at midnight Pacific. — [Google: Indexing API quota](https://developers.google.com/search/apis/indexing-api/v3/quota?authuser=8)
- Since Sept 2024 the docs warn "all submissions through the Indexing API undergo rigorous spam detection" and abuse (including multiple accounts to exceed quota) "may result in access being revoked." — [Search Engine Journal](https://www.searchenginejournal.com/google-adds-spam-warning-to-indexing-api-documentation/526839/); [Search Engine Roundtable](https://seroundtable.com/google-updates-indexing-api-spam-detection-38056.html)
- Google has repeatedly told sites to stop using it for unsupported content and says sites misusing it "often are spammy & low quality." — [SER: Stop using Indexing API for unsupported content](https://www.seroundtable.com/google-indexing-api-unsupported-content-39470.html); [SER: wrongful use often spammy](https://www.seroundtable.com/google-indexing-api-abuse-spammy-low-quality-36919.html)
- An approval form was removed from the docs (Oct 16, per SEJ); SEJ notes it's unclear whether the approval requirement itself changed. — [Search Engine Journal](https://www.searchenginejournal.com/google-indexing-api-docs-approval-form-removed/593292/)

**IndexNow**
- Protocol: put a UTF-8 text file named `{key}.txt` containing the key at the site root (a key file in a subfolder only covers URLs under that folder). Single URL via GET; bulk via POST JSON `{"host","key","keyLocation"(optional),"urlList":[...]}` to `https://api.indexnow.org/indexnow`; up to 10,000 URLs per POST; >10,000 returns HTTP 422. — [IndexNow FAQ](https://indexnow.org/faq); [IndexNow documentation](https://www.indexnow.org/documentation); [Yandex IndexNow reference](https://yandex.ru/support/webmaster/en/indexnow/reference)
- One submission is shared among participating engines: Bing, Yandex, Naver, Seznam, Yep. — [specification.website: IndexNow](https://specification.website/spec/seo/indexnow/); [Wikipedia: IndexNow](https://en.wikipedia.org/wiki/IndexNow); [Bing IndexNow get started](https://bing.com/indexnow/getstarted)
- Microsoft's developer guidance names IndexNow the primary method for real-time URL submission to Bing. — summarized in [PPC Land: Microsoft retires Bing PubHub](https://ppc.land/microsoft-retires-bing-pubhub-submission-platform/)
- Google's stance: Google tested IndexNow in Nov 2021; John Mueller said "don't expect this to go live fully anytime soon"; Gary Illyes (2022) said if Google uses it "it won't be in the format we are thinking about," citing lastmod-style abuse. No 2025–2026 change found; secondary sources in 2025–26 still say Google does not participate. — [SER: Google may use IndexNow](https://www.seroundtable.com/google-indexnow-32396.html); [PPC Land: Google's absence from IndexNow](https://ppc.land/googles-absence-from-indexnow-raises-questions-about-web-indexing-standards/)
- Fabrice Canel (IndexNow champion) retired from Microsoft; IndexNow and Bing Webmaster Tools continue. — [Search Engine Journal](https://www.searchenginejournal.com/fabrice-canel-longtime-bing-search-leader-retires-from-microsoft/)

**WebSub (formerly PubSubHubbub)**
- WebSub is a W3C Recommendation (2018); publishers advertise a `hub` and `self` link (HTTP Link header first, then `<link>` in the feed/HTML) and notify the hub on update. — [W3C WebSub](https://www.w3.org/TR/websub/); [W3C REC 2018](https://www.w3.org/TR/2018/REC-websub-20180123/)

**Speed / why minutes matter**
- Barry Adams: Top Stories are triggered by a simultaneous spike in search volume and publishing volume; news ranking depends on speed, with the useful window sometimes minutes after publication; a story's shelf life in Google's news ecosystem is roughly 48 hours. — [Barry Adams, YoastCon 2023 slides](https://speakerdeck.com/badams/news-seo-is-the-cutting-edge-of-all-seo); [SEOSLY podcast #60 with Barry Adams](https://seosly.com/blog/seo-for-news-websites/); [NewzDash webinar with Barry Adams](https://www.newzdash.com/guide/advanced-tech-seo-news-publishers-barry-adams-webinar)
- Publication frequency influences how often Googlebot recrawls a news site. — [Sitebulb: Ink to Code](https://sitebulb.com/resources/guides/ink-to-code-technical-seo-considerations-for-news-publishers)

**Repo check (this site, 2026-11-21)**
- `docs/news-sitemap.xml` is regenerated by `.github/workflows/news-sitemap.yml` on every push that touches `docs/**/*.html` plus hourly (`23 * * * *`), with a 48-hour window, and the same workflow already POSTs new URLs to `https://api.indexnow.org/IndexNow` using key file `docs/0eb84b5499184e73bd98330eb3641bd3.txt`.
- `<news:publication_date>` is written date-only (e.g. `2026-11-21`), not a full timestamp.
- `docs/robots.txt` lists `sitemap.xml`, `news-sitemap.xml` and `feed.xml`. `docs/feed.xml` has no WebSub `rel="hub"` link.

### Inferences
- Google discovers new news URLs on a well-established news site mainly by recrawling the homepage, section pages, news sitemap and feeds at high frequency; a small site has to earn that crawl rate through publishing frequency and quality, so "within minutes" for Google is a function of crawl demand, not of any push API a small publisher can call.
- The news sitemap should carry full W3C datetime with timezone (e.g. `2026-11-21T14:05:00-08:00`) rather than date-only; Google's spec accepts W3C formats, and a time gives freshness ordering within a day. (Spec wording on accepted formats not re-verified this session — see Gaps.)
- Adding a WebSub hub link to `feed.xml` and pinging a public hub (e.g. Google's `pubsubhubbub.appspot.com`) costs nothing and may help feed readers/aggregators; its effect on Google web search crawling is unproven.
- Never use the Google Indexing API for articles: it is outside policy, quota-limited, and now flagged as a spam signal.

### Gaps
- No primary Google statement found on how fast/how often Googlebot fetches news sitemaps (no official interval exists to my knowledge; practitioners cite "minutes" for big sites).
- Could not verify whether Google currently consumes WebSub pings from `pubsubhubbub.appspot.com` for web search discovery; search returned only the W3C spec.
- Exact allowed `publication_date` formats not re-read this session (page fetch blocked).

---

## 2. Structured data: NewsArticle, authors, LiveBlogPosting, dates, logo, speakable, ClaimReview

### Takeaway
Google's Article/NewsArticle markup has no required properties, only recommended ones; the ones that matter are `headline`, `image` (multiple ratios), `datePublished`/`dateModified` with time and timezone, and `author` as a typed entity with a `url` to an author profile page. ClaimReview rich results were retired in 2025; LiveBlogPosting still drives the "LIVE" badge per industry sources.

### Cited Findings
- Article/NewsArticle/BlogPosting: "There are no required properties; instead, add the properties that apply to your content." More recommended properties = higher-quality result. — [Google: Article structured data](https://developers.google.com/search/docs/data-types/article)
- Images: supply multiple high-resolution images in 16x9, 4x3 and 1x1, each at least 50K pixels (width × height); URLs must be crawlable and indexable and relevant to the page. — [Google: Article structured data](https://developers.google.com/search/docs/data-types/article)
- Author: Google "strongly recommend[s] using the type and url (or sameAs) properties"; if the URL is an internal profile page, mark that page up with ProfilePage structured data; include all authors. — [Google: Article structured data](https://developers.google.com/search/docs/data-types/article)
- Dates: use a CreativeWork subtype with `datePublished` and/or `dateModified` in ISO 8601; time and timezone recommended; `datePublished` should not change; `dateModified` must be later than `datePublished`. — [Google: Influence your byline dates](https://developers.google.com/search/docs/appearance/publication-dates?authuser=2); [Google News: Best practices for article pages](https://support.google.com/news/publisher-center/answer/9607104?hl=en-GB)
- Show one clear visible date and time, ideally between headline and body; for Google News the date must be visible on the page, structured data alone is not enough; avoid showing multiple dates; separate byline and date from the first sentence. — [Google: byline dates](https://goo.gle/byline-date); [Google News: article page best practices](https://support.google.com/news/publisher-center/answer/9607104?hl=en-GB); [Search Engine Land guide](https://searchengineland.com/guide/byline-dates)
- ClaimReview: Google announced on 12 June 2025 it would phase out ClaimReview (and several other types) from Search results; Search Console reporting and Rich Results Test support removed (Sept 9). Rankings unaffected; schema still exists on schema.org; Fact Check Explorer reportedly continues. — [Google Search Central Blog, June 2025](https://developers.google.com/search/blog/2025/06/simplifying-search-results); [Search Engine Land](https://searchengineland.com/google-to-drop-support-for-several-rich-result-types-to-simplify-the-search-results-page-456969); [SER: Search Console drops 6 types](https://www.seroundtable.com/google-search-console-deprecated-structured-data-40083.html); [Nieman Lab](https://www.niemanlab.org/2025/06/google-kills-the-fact-checking-snippet/); [Poynter](https://www.poynter.org/ifcn/2025/google-claimreview-fact-checks-snippets-removed/)
- LiveBlogPosting: a schema.org subtype of Article; publishers using it see a red "LIVE" label on the Top Stories thumbnail; frequent updates are needed to keep the badge. Sources conflict on whether approval is needed (one vendor says markup alone suffices). All are vendor sources. — [Tickaroo](https://tickaroo.com/en/blog/how-to-get-the-red-live-badge-on-google-using-liveblogs); [Norkon](https://www.norkon.net/live-blog-posting-schema/); [Search Engine Land: Google launches LIVE label (2016)](https://searchengineland.com/google-launches-live-label-in-carousel-for-live-blog-publishers-236488)
- Google's 2020 "Best practices for news coverage with Search" post covers live coverage practices. — [Google Search Central Blog, Feb 2020](https://developers.google.com/search/blog/2020/02/best-practices-for-news-coverage-with?hl=en)
- Syndication: Google no longer recommends rel=canonical to avoid duplication by syndication partners; it recommends partners `noindex` the syndicated copy (Danny Sullivan: put noindex in the syndication agreement; otherwise "our systems will try to determine the original"). — [Google News: Avoid article duplication](https://support.google.com/news/publisher-center/answer/9606800?hl=en); [Search Engine Land](https://searchengineland.com/google-no-longer-recommends-canonical-tags-for-syndicated-content-406491); [SER](https://www.seroundtable.com/google-seo-guidance-syndication-partners-35673.html)

**Repo check (this site)**
- Sample `docs/russell-brand-guilty-rape-sexual-assault-verdict.html` JSON-LD: `NewsArticle` with headline, description, one image, `datePublished`/`dateModified` as date-only (`2026-11-06`), `author` as an `Organization` ("News Desk, Newswire Hollywood") with no `url`, `publisher` as `NewsMediaOrganization` with no `logo` or `url`.

### Inferences
- Upgrade every article's JSON-LD (in the template that writes article pages): full ISO 8601 timestamps with timezone; `author` as `Person` with `name` + `url` to an on-site author page (plus `sameAs` to social profiles); `image` array with 1x1, 4x3, 16x9 crops ≥1200px wide; `publisher` with `name`, `url`, `logo`; `mainEntityOfPage`/`url` matching the canonical. Desk bylines ("News Desk") are allowed but forfeit the E-E-A-T signal of a named reporter with a profile page.
- SYNDICATED-IN stories (CLAUDE.md intake path 2): Google's guidance implies the copy on our site should be `noindex` (or the original publisher may ask for it); for content we syndicate OUT, our agreements should require partners to noindex.
- Do not add ClaimReview expecting a rich result. A LiveBlogPosting page (one reused URL, `coverageStartTime`/`coverageEndTime`, `liveBlogUpdate` items each with `headline`/`datePublished`) is the right format for awards nights and premieres.

### Gaps
- Could not retrieve Google's current official page on LiveBlogPosting/LIVE badge requirements (property list and approval status); vendor sources conflict.
- `speakable` status not found in search results this session (historically beta, US English, Google Assistant); treat as unverified, low priority.
- Publisher `logo` specifics for Article markup (Google once required 600x60; current guidance not verified this session).

---

## 3. Images, video, AMP, Core Web Vitals, CDN/caching, GitHub Pages limits

### Takeaway
Discover's large-card treatment needs images ≥1200px wide, >300K pixels, ~16:9, plus `max-image-preview:large` (non-AMP). AMP has not been required for Top Stories since the June 2021 page experience update, and Core Web Vitals are not an eligibility gate. GitHub Pages cannot set custom headers, so Cloudflare (free) in front is the standard workaround for cache control.

### Cited Findings
- Discover large image previews: image at least 1200px wide, >300,000 total pixels, 16:9 recommended (example 1280×720); enabled by `max-image-preview:large` robots setting or by AMP. — [Google: Discover and your website](https://developers.google.com/search/docs/appearance/google-discover?authuser=1)
- Google case study: large images in Discover improved CTR and visits; tag placed in each page's head; introduced 2020. — [Google case study: large images in Discover](https://developers.google.com/search/case-studies/large-images-case-study)
- Unresolved: whether Google checks the file's intrinsic width or rendered width when `sizes` makes the displayed image smaller. — [DEV Community thread](https://dev.to/caodawei3/post-image-for-google-discover-1600)
- AMP: Google's April 2021 post said AMP is no longer required and any page "irrespective of its Core Web Vitals score or page experience status" is eligible for Top Stories; AMP badge removed. Google said this was not reduced commitment to AMP. — [Google Search Central Blog, April 2021](https://developers.google.com/search/blog/2021/04/more-details-page-experience); [Search Engine Land](https://searchengineland.com/amp-wont-be-required-for-googles-top-stories-section-335276); [SER: Top Stories eligibility for all pages](https://www.seroundtable.com/google-top-stories-eligibility-for-all-32995.html)
- A month after the change, almost every story in the Top Stories carousel was still AMP (inertia at big publishers). — [The Register, June 2021](https://www.theregister.com/2021/06/28/google_amp_core_web_vitals/)
- Google News app moved to non-AMP pages and sends readers to publisher pages. — [Search Engine Land](https://searchengineland.com/google-news-app-will-display-non-amp-content-and-send-readers-to-publisher-pages-374291)
- GitHub Pages caching: third-party sources state GitHub Pages sets `Cache-Control: max-age=600` on HTML, does not let you add custom headers, and recommend Cloudflare in front for custom cache rules. (Not verified against GitHub docs.) — [jquery.app Cache-Control builder (GitHub Pages notes)](https://www.jquery.app/tools/cache-control-header-builder/)
- Cloudflare: Cache Rules can add to or replace origin Cache-Control; `s-maxage` sets edge TTL separately from browser `max-age`; Transform Rules can add headers to responses. — [Cloudflare docs: Cache-Control](https://13213614.previews.developers.cloudflare.com/cache/concepts/cache-control/index.md); [Cloudflare blog: CDN-Cache-Control](https://blog.cloudflare.com/cdn-cache-control/); [Simon Willison TIL: Cloudflare Transform Rule](https://til.simonwillison.net/cloudflare/cache-control-transform-rule)

**Repo check**: `wire.py` line ~470 emits `<meta name="robots" content="index,follow,max-image-preview:large">`; the sample article page carries the same tag and a self-referencing canonical. Sample article image: one URL only.

### Inferences
- For a static site, Core Web Vitals are easy wins (no server render, no ad stack yet): set explicit `width`/`height` on images, serve hero images as WebP/AVIF with a ≥1200px source, avoid render-blocking web fonts. CWV is not a Top Stories gate, but it is a ranking/page-experience input.
- GitHub Pages' 10-minute HTML cache only affects browsers/CDNs, not Googlebot's ability to fetch; a fresh story is reachable as soon as the Pages deploy finishes. The real latency on this stack is the Actions pipeline (commit → Pages build/deploy → sitemap job → IndexNow), which should be chained in one workflow rather than relying on the hourly schedule.
- Cloudflare free tier in front of GitHub Pages is optional; its main value would be custom headers (e.g., `X-Robots-Tag`, `Link: rel=hub`) and short edge TTL on `news-sitemap.xml`/`feed.xml` plus longer TTL on images. Adding it changes DNS for the domain — Terry's decision.
- Video: VideoObject markup and a crawlable video page are needed for video results; only livestreams (BroadcastEvent) qualify for the Indexing API.

### Gaps
- GitHub Pages official limits (site size, bandwidth, build limits, deploy times, cache TTL) were not verified from GitHub docs this session.
- Current Google VideoObject required properties not retrieved.
- No primary data found on CDN setups at specific major publishers.

---

## 4. URLs, headlines, developing stories, canonicals

### Takeaway
Google picks headlines and dates algorithmically from visible page content and markup, so the `<title>`, `<h1>`, `og:title` and JSON-LD `headline` should agree and lead with the searchable entity. Big publishers split between one evergreen/"live" URL updated over time and fresh URLs per development; both work, with the evergreen URL accumulating links and the fresh URL resetting freshness.

### Cited Findings
- Google News determines headlines with a crawler; publishers should follow its title guidelines so the right headline displays, and separate byline/date from body text. — [Google News: article page best practices](https://support.google.com/news/publisher-center/answer/9607104?hl=en-GB)
- Barry Adams is "not a fan of dates in URLs" but has not seen them hurt rankings; NYT uses different URL formats for evergreen vs time-sensitive content. — [Search Engine Journal: NYT news SEO tips](https://www.searchenginejournal.com/top-news-seo-tips-nytimes/424911)
- Some publishers give ongoing coverage a fresh URL to stay eligible for Top Stories, conflicting with the reuse-one-URL approach. — [Lumar: SEO for news publisher websites](https://www.lumar.io/blog/best-practice/seo-for-news-publisher-websites)
- Google's 2020 news-coverage best practices recommend practices for developing stories and live coverage (including live blog markup). — [Google Search Central Blog, Feb 2020](https://developers.google.com/search/blog/2020/02/best-practices-for-news-coverage-with?hl=en)
- Syndication canonical rule: see Section 2 (noindex, not canonical). — [Search Engine Land](https://searchengineland.com/google-no-longer-recommends-canonical-tags-for-syndicated-content-406491)

### Inferences
- Pattern for this site: keyword-first `<title>`/SEO title (who + what, under ~60–70 chars to avoid truncation), a slightly more voiced on-page `<h1>`, both containing the main entity name; short, stable, keyword slugs without dates (current `slug.html` pattern already fits); update the same URL with a bumped `dateModified` and visible "Updated" time for incremental developments; publish a new URL when the story materially changes (verdict, death, deal close), linking back to the original.
- Hub/tag pages per recurring entity (e.g., an Emmys page like `docs/emmys-2026.html`) act as the evergreen URL big publishers reuse.

### Gaps
- No official Google statement found on title length or keyword-first headlines; practitioner guidance only (not retrieved this session).
- Datelines: no source found tying datelines to ranking.

---

## 5. Distribution feeds: Google News Publisher Center, Bing PubHub, MSN, Apple News, Yahoo

### Takeaway
Since 2024–2025, Google News is fully automatic: Publisher Center no longer uses submitted RSS feeds, sections, or manual publication pages, and eligibility is earned through crawling of the site itself. Bing PubHub closed to new applicants in 2025, replaced by algorithmic inclusion plus IndexNow. Apple News still accepts RSS via News Publisher.

### Cited Findings
- Google News transitioned to automatically generated publication pages (announced Feb 10, 2025, following April 2024 changes): Google News "will no longer use RSS feeds or web locations that were submitted in Publisher Center"; manual publication pages and custom sections no longer appear; RSS article text no longer rendered in the app; custom analytics IDs, tracking pixels, RSS styling and feed ads removed; Publisher Center stopped accepting publications; content eligibility for Google News is unchanged. — [Google News Publisher Help](https://support.google.com/news/publisher-center/answer/15898024); [SER](https://www.seroundtable.com/google-news-automatically-generated-publications-39149.html); [Search Engine Land](https://searchengineland.com/google-news-automated-publication-pages-to-start-in-march-451831); [PPC Land](https://ppc.land/google-news-shifts-to-automated-publication-pages/)
- Bing PubHub: Microsoft (June 2025) stopped accepting new publisher applications; sites already in the Bing News index remain; PubHub membership does not influence Bing News ranking; IndexNow is the recommended real-time submission method. — [SER: Microsoft is retiring Bing PubHub](https://www.seroundtable.com/bing-pubhub-retired-39552.html); [PPC Land](https://ppc.land/microsoft-retires-bing-pubhub-submission-platform/)
- Apple News: RSS items need title, link, description; full-text RSS recommended, short-form supported; `atom:link rel="self"` required; thumbnail/author pulled from article HTML; no backfill of older articles once live; RSS channels reportedly cannot monetize (vendor claim). One CMS vendor claims RSS no longer supported — contradicted by Apple's own guide. — [Apple News Publisher guide](https://support.apple.com/en-gu/guide/news-publisher/apdc2c7520ff/icloud); [Craft CMS (conflicting claim)](https://craftcms.com/knowledge-base/publishing-content-to-apple-news); [Apple News Format resources](https://developer.apple.com/apple-news/resources)

### Inferences
- There is no "submit to Google News" step anymore for this site; the news sitemap, crawlable section pages, visible dates/bylines, and clear publisher identity (About, contact, masthead, editorial policies) are the whole application.
- `docs/feed.xml` doubles as the Apple News source; it should carry full text (our own originated stories only — never syndicated-in text), `atom:link rel="self"`, and per-item images.

### Gaps
- MSN Partner Hub / Microsoft Start technical ingestion requirements: no current source found (partner programme is invitation/application based; specs not retrieved).
- Yahoo News ingestion: no current source found.
- Whether Bing News fully closed PubHub (end date) is unconfirmed.

---

## 6. Priority checklist for a static GitHub Pages news site (synthesis)

### Takeaway
Most of the high-value plumbing already exists in this repo (48-hour news sitemap regenerated on push + hourly, IndexNow on publish, `max-image-preview:large`, NewsArticle JSON-LD, canonicals, RSS). The remaining gains are in markup quality (timestamps, authors, image ratios, logo), feed enrichment, and chaining the publish pipeline so discovery signals fire within a minute or two of a push.

### Cited Findings
(Each item rests on findings cited in Sections 1–5.)
1. News sitemap, 48h window, ≤1,000, exact publication name, regenerated on publish — [Google News sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en)
2. Sitemaps declared in robots.txt + submitted in Search Console (no ping) — [Google blog 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)
3. Accurate `lastmod`/`dateModified` only on substantive change — [Google blog 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping); [Google byline dates](https://goo.gle/byline-date)
4. IndexNow POST on publish/update — [IndexNow FAQ](https://indexnow.org/faq)
5. NewsArticle JSON-LD: timestamps with TZ, Person author + url, 3 image ratios — [Google Article docs](https://developers.google.com/search/docs/data-types/article)
6. Visible date/time and byline near headline — [Google News article best practices](https://support.google.com/news/publisher-center/answer/9607104?hl=en-GB)
7. ≥1200px 16:9 lead image + `max-image-preview:large` + og:image — [Google Discover docs](https://developers.google.com/search/docs/appearance/google-discover?authuser=1)
8. No AMP needed — [Google blog 2021](https://developers.google.com/search/blog/2021/04/more-details-page-experience)
9. Syndicated-in copies noindexed (or attributed per agreement) — [Google News duplication](https://support.google.com/news/publisher-center/answer/9606800?hl=en)
10. LiveBlogPosting for live events — [Tickaroo](https://tickaroo.com/en/blog/how-to-get-the-red-live-badge-on-google-using-liveblogs)

### Inferences
Recommended order of work for Newswire Hollywood (repo-specific, from repo check):
1. **Timestamps everywhere** — change JSON-LD `datePublished`/`dateModified` and `<news:publication_date>` from date-only to full ISO 8601 with Pacific offset; show a visible "Published 2:05 PM PT · Updated 4:40 PM PT" line under the headline.
2. **Author identity** — named Person bylines with on-site author pages (ProfilePage markup, bio, credentials, social `sameAs`); keep "News Desk" only for true desk copy.
3. **Image set** — generate 1x1, 4x3, 16x9 crops (≥1200px wide) per lead image in the build script; list all three in JSON-LD `image`; record license source per CLAUDE.md image rules.
4. **Publisher block** — add `url`, `logo` (ImageObject), `sameAs` to the `NewsMediaOrganization`; matching About/Masthead/Corrections/Ethics pages (Google News eligibility is judged from the site itself now).
5. **One chained publish workflow** — on push: wait for Pages deploy, regenerate news sitemap + sitemap `lastmod` + feed, then IndexNow for new/updated URLs only (already mostly in place; confirm it runs after the Pages deploy succeeds, not before).
6. **Feed upgrades** — full-text items for originated stories, `atom:link rel="self"`, `rel="hub"` WebSub link and hub ping (zero cost), per-item image enclosure; apply to Apple News Publisher.
7. **Live coverage template** — a LiveBlogPosting page type for awards shows/premieres (one URL, timestamped updates).
8. **Optional** — Cloudflare free in front for headers/edge TTL (DNS change, Terry's call); Bing Webmaster Tools verification (to see IndexNow acceptance); Search Console News/Discover reports.
Monetization angle: faster indexing directly raises ad-impression volume on breaking stories; Discover large-image cards are the biggest CTR lever per Google's own case study.

### Gaps
- No measured benchmark found for how quickly Google indexes a small, new news site's articles versus established publishers.
