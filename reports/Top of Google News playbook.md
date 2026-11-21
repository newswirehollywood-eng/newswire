# Beating the Giants to Google's Top Stories

*Research report for Terry Bryant, Newswire Hollywood. As of 21 November 2026. Applies to Newswire Hollywood, Hollywood News Access, Gospel News Access, World Newswire Press and PR STARPOWER.*

The big publishers do not have a secret "submit to Google" button. CNN, the New York Times, People and the rest get breaking stories into Google's Top Stories within minutes because Google already trusts them and checks their sites almost constantly. They earned that by being the source other outlets cite, by publishing fast, and by keeping clean, honest technical signals. Google has no fast lane a small publisher can pay for or switch on. Bing and the engines that use its index do have one, called IndexNow, and Newswire already uses it. **The top 1,000 domains held 97.3% of all Top Stories listings in a 2024 study** ([Detailed.com](https://detailed.com/top-stories)), and small sites lost about 60% of their search referrals over two years ([Search Engine Journal on Chartbeat](https://www.searchenginejournal.com/google-search-decline-publishers-chartbeat/590681/)). Head-to-head speed against TMZ on a national celebrity story is not a fight we can win. The 2026 updates opened a different door. Google's first Discover-only update (February 2026) rewards local, original, specialist sites and demotes clickbait and aggregators ([Google Search Central](https://developers.google.com/search/blog/2026/02/discover-core-update)). Discover (Google's personalized article feed on phones) now carries roughly two-thirds of Google's news traffic ([Search Engine Roundtable](https://www.seroundtable.com/google-search-traffic-drops-news-publishers-40645.html)). So the plan is four things. Own beats the giants cover thinly: Los Angeles events, credentialed red carpets, gospel and faith entertainment. Fix five technical gaps in our story pages, all free. Run a disciplined "first 15 minutes" routine. Open the distribution channels that still accept small publishers. Most of the plumbing is already built in our repo, and most of this plan costs nothing.

---

## How to read this report

**Honesty flag, kept from the research notes.** Our research sessions could not open many key websites directly: Google's developer pages, Press Gazette, NewzDash, Search Engine Land and others were blocked by the network. Many findings therefore come from **search-engine summaries of those pages, not full reads**. Where a figure conflicts across sources, comes from a vendor's sales blog, or rests on one report, this report says so. Before any number here goes into a published book or a client deck, check it on the source page.

**Ten words you will hear, in plain English.**

| Term | What it means |
|---|---|
| Top Stories | The box of news headlines Google shows at the top of a search. |
| Google News | Google's news app and website, plus the "News" tab in search. |
| Discover | The personalized feed of articles on the Google app and Chrome's new-tab page on phones. No search needed. It is now Google's biggest news traffic source. |
| Crawl / index | Google's robot visits a page (crawl), then files it so it can appear in results (index). |
| Structured data / schema / JSON-LD | Hidden labels in a web page that tell machines "this is a news article, here is the headline, author, time and photo." JSON-LD is the format we use. NewsArticle is the label type. |
| News sitemap | A machine-readable list of our stories from the last two days, which Google reads to find new articles. |
| IndexNow | A free "doorbell" that instantly tells Bing, Yandex, Naver, Seznam and Yep that a page is new or changed. Google does not answer it. |
| RSS feed / WebSub | RSS is a running list of our newest stories that apps read. WebSub is a free add-on that rings the apps the moment the list changes. |
| Topic authority | Google's judgment of who is the real expert source on a subject or place, measured partly by how often other outlets cite their original reporting. |
| Preferred Sources | A Google feature where a reader stars a publisher so it shows up more often for them in Top Stories. |

---

## A thousand brands hold 97% of Top Stories, and the leaders are shrinking

### The ranked landscape, with what the evidence can and cannot support

News search is a closed shop at the top. In the 2024 Detailed.com and NewzDash study of about 45 million keywords, **the 1,000 most visible domains held 97.3% of Top Stories listings, and 704 of them were established media brands** ([Detailed.com](https://detailed.com/top-stories)). A few PR distribution services, government sites and even betting companies also got in ([Press Gazette](https://pressgazette.co.uk/platforms/pr-and-betting-companies-have-articles-indexed-in-google-top-stories/)). Outsiders can get in, but rarely. The study uses 2024 data.

The table ranks what our sources actually support. Some of the publishers Terry named do not appear with a confirmed rank in any source we could read: TMZ, Variety, Deadline, THR, E!, US Weekly, ET, ABC, CBS, NBC, BBC, AP and Reuters. **Those rows are marked unconfirmed rather than guessed.**

| Tier | Publisher | What the evidence shows | Confidence |
|---|---|---|---|
| 1 | **New York Times** | #1 US news site by traffic. The only top-10 English-language site to grow year on year, about +11% (October 2026 data). Top "Live" Top Stories spot at the 2025 Met Gala with 17% visibility. A winner in the March 2026 core update. ([Press Gazette world top 50](https://pressgazette.co.uk/most-popular-websites-news-world-monthly/); [ppc.land](https://ppc.land/nyt-traffic-gains-11-as-only-10-of-top-50-english-language-news-sites-grow/); [NewzDash Met Gala](https://www.newzdash.com/guide/met-gala-2025-top-news-publishers-seo-winners-dominating-google)) | High. Monthly visit totals conflict across editions (roughly 400M to 593M). |
| 1 | **CNN** | #1 overall and in Headlines in NewzDash's 2025 US Top Stories review (3.5M Top Stories rankings counted). About 431M visits in one 2026 month, down about 35% year on year. ([NewzDash 2025](https://newsdashboard.com/en/u-s-year-in-review-2025-google-news-visibility-across-categories/); [Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/media_metrics/most-popular-websites-news-world-monthly-2/)) | High on Top Stories. The month of the traffic figure is unconfirmed. |
| 1 | Fox News | About 223M visits in the same 2026 month, down about 36%. ([Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/media_metrics/most-popular-websites-news-world-monthly-2/)) | Medium |
| 2 (entertainment) | **People.com, Page Six** | Led Google Top Stories for the 2025 Met Gala alongside NYT. ([NewzDash](https://www.newzdash.com/guide/met-gala-2025-top-news-publishers-seo-winners-dominating-google)) | High for that event |
| 2 | The Guardian | Biggest gainer, with NYT, in the March 2026 core update. ([Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/march-google-core-update-brings-modest-gains-for-news-websites/)) | Medium |
| 2 | Daily Mail | Among the biggest year-on-year traffic losers in August 2026, with Newsweek and Business Insider. ([Press Gazette US monthly](https://pressgazette.co.uk/most-popular-websites-news-us-monthly/)) | Medium |
| 2 | Yahoo / Yahoo Finance | Yahoo's share of Discover fell after the February 2026 update. Yahoo Finance lost in March 2026. ([Search Engine Journal](https://www.searchenginejournal.com/google-discover-update-early-data-shows-fewer-domains-in-us/568091/); [Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/march-google-core-update-brings-modest-gains-for-news-websites/)) | Medium. Yahoo's overall rank is unconfirmed. |
| 2 | AP, Reuters | Their power is licensing, not search rank. AP is among the outlets Microsoft licenses for its AI products. Reuters runs a content-trading marketplace. ([capconvert](https://www.capconvert.com/learn/blog/microsoft-ads-in-2026-copilot-integration-publisher-marketplace-and-what-s-new); [Digiday](https://digiday.com/media/reuters-building-marketplace-video-hungry-publishers)) | Medium (secondary sources) |
| Unconfirmed | TMZ, Variety, Deadline, THR, E!, US Weekly, ET, MSN, ABC, CBS, NBC, BBC | NewzDash publishes a "US Entertainment Top 100" ranked by Top Stories visibility, but its rows could not be read ([NewzDash](https://ww2.newzdash.com/about/all-news-publishers-tracked/U.S./2/Entertainment/)). One opinion blog calls People the trusted authority, TMZ the fastest and Page Six the most sensational. That is opinion only ([The World Beast](https://www.theworldbeast.com/people-magazine-vs-tmz-vs-page-six-seo-comparison.html)). | Not established. Re-check the NewzDash list quarterly. |

The giants are also losing ground. **Visits to the 50 biggest US news sites fell 37% from July 2024 to July 2026**, and the top ten lost almost a third ([Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/media_metrics/traffic-to-10-biggest-us-news-websites-down-a-third-in-two-years/)). Four in five of the top 50 lost traffic in October 2026 ([Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/media_metrics/most-popular-websites-news-us-monthly-3/)). Small sites were hit harder. Chartbeat measured a **60% two-year fall in search referrals for sites with 1,000 to 10,000 daily page views, against 22% for large sites** ([Search Engine Journal](https://www.searchenginejournal.com/google-search-decline-publishers-chartbeat/590681/)). Press Gazette reported the same 60% figure as a 2025-only fall, so the timeframe conflicts between write-ups ([Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/us-publishers-see-traffic-boost-for-breaking-news-from-google-discover/)).

### Why the leaders win: trust earned in advance, then speed

The giants win "within minutes" because of crawl demand, not a button. Google sends its robot back to a big publisher's homepage, section pages and news sitemap so often that a new story is found almost at once. Barry Adams, the most-cited news SEO consultant, says Google tends to crawl and index a news publisher's story within a few minutes, and it can appear in Top Stories almost immediately ([Eric Schwartzman interview](https://www.ericschwartzman.com/news-seo-barry-adams/)). How often Google comes back depends partly on how often a site publishes ([Sitebulb](https://sitebulb.com/resources/guides/ink-to-code-technical-seo-considerations-for-news-publishers)). A small site has to earn that attention with steady, trusted output. **No official Google figure says how often it checks a news sitemap.** This is the honest answer to "how do they get there in minutes."

Three habits explain the rest, and all three are copyable. First, they are cited. Google's topic authority system looks at how often other publishers cite an outlet's original reporting on a subject or locality ([Google Search Central](https://developers.google.com/search/blog/2023/05/understanding-news-topic-authority)). Second, they prepare. People's staff write "pre-writes" for awards shows, so the winner story exists before the envelope opens ([Built In listing](https://builtin.com/job/summer-intern-people-editorial/4077696)). People's parent company says the brand has more than 250 journalists ([Google Play listing](https://play.google.com/store/apps/details?id=com.dotdashmdp.people&hl=en)). Third, they go live. NYT's 17% "Live" share at the Met Gala shows that live coverage pages take the top Top Stories slot at big events ([NewzDash](https://www.newzdash.com/guide/met-gala-2025-top-news-publishers-seo-winners-dominating-google)).

### Discover is now the front door, and breaking news is the one growing lane

**Discover rose from 37% to about 67.5% of Google's traffic to publishers, while regular search fell from 51% to about 27%** (NewzDash, 400+ publishers) ([Search Engine Roundtable](https://www.seroundtable.com/google-search-traffic-drops-news-publishers-40645.html)). Sources date the 67.5% figure differently: one says Q4 2024, another a late-2025 post ([PPC Land](https://ppc.land/news-publishers-lose-half-their-google-search-traffic-in-two-years/)). Discover's own traffic also fell 21% in the year to November 2025, so its larger share partly reflects search falling faster ([Press Gazette](https://pressgazette.co.uk/comment-analysis/google-discover-traffic-news-websites-2025/)). The bright spot is breaking news. **Google referrals for breaking news to US publishers roughly doubled (+103%) from November 2024, mostly via Discover** ([Press Gazette, search summary](https://pressgazette.co.uk/media-audience-and-business-data/us-publishers-see-traffic-boost-for-breaking-news-from-google-discover/)). Breaking news is the part of the business Google is still rewarding.

### Bing, MSN, Yahoo and Apple News each have a different door

The "within minutes" answer changes by platform. For **Bing** (which also powers Copilot and DuckDuckGo), the instant door is **IndexNow**, which Microsoft names its main real-time submission method ([PPC Land](https://ppc.land/microsoft-retires-bing-pubhub-submission-platform/)). Newswire already rings it on every publish. **MSN** takes stories from invited partners only. Microsoft's own page says Partner Hub is invitation-only ([Microsoft Support](https://support.microsoft.com/en-us/msn/partner-hub/how-to-set-up-your-msn-partner-hub-account)). **Yahoo News** runs publisher syndication through partner managers, not an open application ([Built In](https://builtin.com/job/editorial-partner-manager-curation/4561237)). **Apple News** reads an RSS feed through its News Publisher tool, but reportedly stopped taking unsolicited applications in 2025 ([Publisher in a Box](https://publisherinabox.com/apple-news-for-publishers)). Big brands are fast on MSN, Yahoo and Apple because they hold contracts that pipe stories in automatically. That is a business-development job, covered in the distribution section.

### Where a small site can actually dominate

Domination for us means owning the searches where the giants are slow, absent or not local. Three lanes fit what Google's 2026 updates reward. The first is **Los Angeles events and credentialed red carpets**. The February 2026 Discover update favors locally relevant content from sites in the reader's country ([Google](https://developers.google.com/search/blog/2026/02/discover-core-update)), and RebelMouse said local sites in its network gained most ([RebelMouse](https://www.rebelmouse.com/2026-google-discover-algorithm-update)). The Events Calendar division is the engine for this. The second is **gospel and faith entertainment**. The faith news leader, The Christian Post, draws only about 2 to 3 million visits a month ([FeedSpot](https://www.feedspot.com/blog/christian-news-sources/); [Similarweb](https://www.similarweb.com/website/christianpost.com/competitors/)). Christianity Today drew about 1.3 million over three months ([Similarweb](https://www.similarweb.com/website/christianitytoday.com/)). This is our inference, not a sourced finding: a mid-sized niche with no giant in it is where Gospel News Access can build topic authority fastest. The third is **the best follow-up**. Adams says that if you cannot be first, the best article can still win more traffic ([Press Gazette, search summary](https://pressgazette.co.uk/platforms/google-news-seo-tips-publishers/)).

World Newswire Press is the hardest lane. World news from a small US site competes with BBC, Reuters and the Guardian, and Discover now favors in-country sources. Our inference is that World Newswire should lead with US-angle international stories, such as international films opening in the US or diaspora communities, rather than general world headlines.

---

## Google rewards the source others cite, and the fastest clean page

Google's own list of news ranking factors is **relevance, prominence, authoritativeness, freshness, location and language**. Google says it does not rank by political viewpoint, and that buying ads does not help ([Google, How news works](https://www.google.ca/search/howsearchworks/how-news-works)). On top of that sits topic authority. Google measures influence by **how much a publication's original reporting is cited by other publishers**, plus reputation such as a record of original reporting or journalism awards. Google built it to help local publishers appear for news in their area ([Google Search Central](https://developers.google.com/search/blog/2023/05/understanding-news-topic-authority)). For us, a scoop that Variety credits ("as first reported by Newswire Hollywood") is worth more than ten rewrites. Google's Search Liaison says topic authority has run "for several years," even though it is missing from Google's official list of ranking systems ([Search Engine Journal](https://www.searchenginejournal.com/google-topic-authority/487603/)).

Transparency is the next layer. Google asks news sources for **clear dates, bylines, author information, publisher identity and contact details** ([Google News policies](https://support.google.com/news/publisher-center/answer/6204050)). It has described looking for bylines that link to author bio pages, and for site-level signals such as a mission statement and funding information ([Google Search Central, 2021](https://developers.google.com/search/blog/2021/06/google-news-sources)). Since Google stopped taking applications, these pages are effectively the whole application.

Experienced practitioners add four signals that Google has not confirmed but consistently describes. **Speed and crawlability.** Adams calls speed "the defining difference" in news SEO. Google cannot wait to run a page's JavaScript before ranking a breaking story, so the story must arrive as finished HTML ([NewzDash webinar](https://www.newzdash.com/guide/advanced-tech-seo-news-publishers-barry-adams-webinar)). Our static pages already do this. **The headline in the schema.** Adams considers the NewsArticle headline the most important one for Top Stories. Google usually displays the on-page H1 (the big headline at the top). Top Stories truncates at about 70 to 80 characters, so the named person or title should come first ([SEO for Google News](https://www.seoforgooglenews.com/p/the-5-seo-article-headlines-google)). **Accumulated trust and a tight beat**, with specific main categories that match the beat ([SEO for Google News](https://www.seoforgooglenews.com/p/structured-data-for-news-publishers)). **Engagement for Discover.** Discover uses the same core quality systems as search but leans harder on personalization and engagement ([Advanced Web Ranking](https://www.advancedwebranking.com/blog/news-seo-ai-search)). A strong search foundation is a main factor in stable Discover visibility ([Search Engine Roundtable](https://www.seroundtable.com/google-search-traffic-drops-news-publishers-40645.html)).

Discover headlines are a balancing act. Lily Ray has observed that headlines which hold back information do better in Discover but worse in search ([WTF is SEO?, search summary](https://www.seoforjournalism.com/p/headlines-news-seo)). Google's February 2026 update then demoted sensationalism and clickbait. Discover sometimes uses the social headline (og:title, the headline shown when a link is shared) instead of the page headline ([SEO for Google News](https://www.seoforgooglenews.com/p/the-5-seo-article-headlines-google)). Our house rule: name the person and the news plainly, and put the voice in the wording, the way Bossip built its brand on "punchy and often alliterative" headlines ([Essence](https://www.essence.com/news/money-career/aiesha-letman-shade-room-black-media-twitter-journalism/)). Never withhold the fact or promise more than the story delivers. Two claims remain unproven: whether click-through rate and links directly affect news rankings, and how much publishing speed matters in a controlled test. No 2025 or 2026 study we found measured either.

---

## 2025 and 2026 rewrote the rules toward original, local and clearly labeled

| When | Change | What it means for us | Source |
|---|---|---|---|
| June 2025 | Google phased ClaimReview (fact-check) rich results out of Search | Do not build fact-check markup expecting a search badge | [Google](https://developers.google.com/search/blog/2025/06/simplifying-search-results) |
| June 2025 | Bing PubHub closed to new publishers. IndexNow is the route in | Already wired on Newswire. Add to sister sites | [SER](https://www.seroundtable.com/bing-pubhub-retired-39552.html) |
| Aug 2025 to Aug 2026 | **Preferred Sources** launched in the US and India (Aug 2025), expanded to English worldwide (Dec 2025), then to more languages, AI Overviews and AI Mode. A publisher "add us" button arrived on 20 Aug 2026. Google says people are about twice as likely to click a preferred source | Free. Add the button to every article on every brand | [Google](https://blog.google/products/search/preferred-sources/); [TechCrunch](https://techcrunch.com/2026/08/20/google-gives-publishers-a-new-way-to-fight-ai-driven-traffic-losses/); [Search Central docs](https://developers.google.com/search/docs/appearance/preferred-sources) |
| Sept 2025 | Discover **Follow**: readers follow publishers. Followed sources' X, Instagram and YouTube Shorts posts can appear in Discover | Social posts become Discover inventory | [Google](https://blog.google/products-and-platforms/products/search/personalize-search-discover-news/) |
| Dec 2025 | Harsh core update. 52 of 75 UK news sites lost visibility. Some publishers' Discover traffic collapsed (one reported a 98% drop) | Even established sites can lose Discover overnight. Do not depend on one channel | [Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/times-and-substack-among-few-uk-winners-from-google-december-2025-core-update/); [PPC Land](https://ppc.land/googles-december-update-destroys-discover-traffic-for-news-sites/) |
| 5 to 27 Feb 2026 | **First Discover-only core update.** More local, in-country content and in-depth original work from topical experts. Less sensationalism and clickbait. Unique publishers in the US Discover top 1,000 fell from 172 to 158 | The biggest opening for an LA-focused original-reporting outlet | [Google](https://developers.google.com/search/blog/2026/02/discover-core-update); [SEJ](https://www.searchenginejournal.com/google-discover-update-early-data-shows-fewer-domains-in-us/568091/) |
| Mar to Apr 2026 | Core update. Guardian, NYT and Substack gained. Yahoo Finance fell | Primary sources beat repackagers | [Press Gazette](https://pressgazette.co.uk/media-audience-and-business-data/march-google-core-update-brings-modest-gains-for-news-websites/) |
| 21 May to 2 June 2026 | Core update. Visibility shifted from aggregators to primary destinations ("authority beats interchangeability," per a Sistrix summary) | Our wire cards help readers but will not carry our search ranking. Originated stories will | [triaza (secondary)](https://triaza.com/blog/seo/google-may-2026-core-update/) |
| Mar, Jun, Sep 2026 | Spam updates, including scaled content abuse. Reports conflict in detail | No mass-produced pages, AI-written or not | [Digital Applied](https://www.digitalapplied.com/blog/google-june-2026-spam-update-rollout-site-owner-guide) |
| Aug 2026 | Google published a further site reputation abuse policy update. **Its contents were not verified** | Re-read before scaling sponsored or PR content on news domains | [Google](https://developers.google.com/search/blog/2026/08/update-site-reputation-policy) |
| Unverified | A "November 2026 core update" appeared in one search result with no corroboration | Check Google's status dashboard before reacting | n/a |

**AI Overviews (the AI-written summary box at the top of Google results) cut clicks, but entertainment has a way in.** In Pew's browsing panel, people clicked a regular result on 8% of visits when an AI summary appeared, against 15% without one. Links inside the summary got about 1% ([Search Engine Journal](https://www.searchenginejournal.com/impact-of-ai-overviews-how-publishers-need-to-adapt/556843/)). Zero-click estimates range from 22% to 69% depending on method ([The Next Web](https://thenextweb.com/news/google-ai-overviews-publisher-links-search-traffic)). Google now places a Top Stories carousel inside AI Overviews, and **entertainment is the category most likely to trigger it: 35% of the time in the US** ([NewzDash](https://www.newzdash.com/guide/top-stories-ai-overviews-data-strategy-and-impact-blocking-google-ai); [Press Gazette](https://pressgazette.co.uk/platforms/google-adds-top-stories-links-to-many-news-related-ai-summaries/)). NewzDash also found that Top Stories lead while an event is live, and AI Overviews take over once coverage slows ([NewzDash](https://www.newzdash.com/guide/newzdash-2025-study-how-google%E2%80%99s-ai-overviews-are-impacting-news-visibility-search)). For an entertainment outlet, being in the carousel during the live window is now worth more, and the slow-news summary is worth less. AI chatbots are still a small news habit. **Weekly use for news reached 10% in 2026 (17% among 18 to 24-year-olds), and only 1% call AI their main news source** ([Reuters Institute](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism)).

**Site reputation abuse is the 2026 trap for a publisher that also sells PR.** The policy targets third-party or sponsored content that rides a host site's ranking strength ([Google](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)). Google enforced it with manual penalties (a human reviewer demotes or removes part of a site) against CNN Underscored, WSJ Buyside and coupon sections at CNN, USA Today and the LA Times ([Search Engine Journal](https://www.searchenginejournal.com/big-brands-receive-site-abuse-manual-actions/515729/); [Search Engine Land](https://searchengineland.com/google-begins-enforcement-of-site-reputation-abuse-policy-with-portions-of-sites-being-delisted-440294)). Google's November 2024 update says the host's own involvement does not excuse it, and a penalty hits only the offending section ([Google](https://developers.google.com/search/blog/2024/11/site-reputation-abuse?hl=en)). The UK publishers' body AOP says "third party" now covers freelancers too ([Press Gazette](https://pressgazette.co.uk/comment-analysis/google-site-reputation-abuse-policy-publishers-aop/)). The European Commission opened a Digital Markets Act investigation into the policy on 13 November 2025. Its outcome was not found ([ppc.land](https://ppc.land/site-reputation-abuse/)). Our PAID OUT intake path is exactly the content this policy watches. The repo section below explains what to do.

---

## Our plumbing is mostly built. Five free fixes finish it

### What a check of the repo found on 21 November 2026

Newswire is ahead of most small publishers. `.github/workflows/news-sitemap.yml` rebuilds `docs/news-sitemap.xml` (a 48-hour window) on every push that touches a story page and hourly as a backup. The same workflow sends new URLs to IndexNow using the key file `docs/0eb84b5499184e73bd98330eb3641bd3.txt`. Pages carry `max-image-preview:large`, which lets Discover show big photos, plus self-referencing canonical tags (a canonical tag tells Google "this is the official copy of this page"). `docs/robots.txt` lists the sitemaps and the feed. `docs/feed.xml` already carries full text (`content:encoded`) and the required `atom:link rel="self"`. Those all match Google's and IndexNow's published rules ([Google news sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en); [IndexNow](https://indexnow.org/faq)).

The gaps, confirmed by reading `docs/russell-brand-guilty-rape-sexual-assault-verdict.html` and the workflow:

| Gap found | Where | Why it matters |
|---|---|---|
| **Dates without times.** `"datePublished": "2026-11-06"` in the schema, and `<news:publication_date>` written date-only (workflow line ~111) | Article template, news-sitemap workflow | Google recommends ISO 8601 dates with time and time zone, for example `2026-11-06T14:05:00-08:00` ([Google byline dates](https://developers.google.com/search/docs/appearance/publication-dates?authuser=2)). In a breaking race, a story stamped "today" cannot show it came first that day. The visible date and the schema date must match ([Google News best practices](https://support.google.com/news/publisher-center/answer/9607104?hl=en-GB)). |
| **Organization-only author.** `"author": {"@type": "Organization", "name": "News Desk, Newswire Hollywood"}` with no link | Article template | Google "strongly recommends" a typed author with a `url` pointing to a profile page marked up as ProfilePage ([Google Article docs](https://developers.google.com/search/docs/data-types/article)). Named people with bios are the transparency signal Google News asks for. No author pages exist in `docs/`. |
| **Single image.** One URL (a 1600×2000 portrait JPEG) | Article template, image pipeline | Google asks for 16:9, 4:3 and 1:1 versions. Discover's large cards need images at least 1200px wide, about 16:9 ([Google Discover docs](https://developers.google.com/search/docs/appearance/google-discover?authuser=1)). A tall portrait crops badly in Discover. |
| **Publisher block without logo.** `NewsMediaOrganization` with a name only: no `url`, `logo` or `sameAs` | Article template | Weak publisher identity. Since Google News stopped taking applications, identity is judged from the site itself ([Google News Help](https://support.google.com/news/publisher-center/answer/15898024)). Exact logo dimensions were not re-verified. |
| **No WebSub.** `docs/feed.xml` has no `rel="hub"` link | Feed generator | WebSub is a W3C standard that pushes feed updates to readers and apps instantly ([W3C](https://www.w3.org/TR/websub/)). Free. **Its effect on Google crawling is unproven.** |
| **Trust pages not linked.** No About, masthead, contact, corrections or ethics page links found from `docs/index.html` or `docs/_template-article.html`. The October distribution guide says some exist; confirm where | Site footer, `wire.py` | Google News, NewsBreak and MSN all check for them ([NewsBreak criteria](https://support.newsbreak.com/knowledge/application-review-process-and-approval-criteria)). |
| **No Preferred Sources button** | Article template | A free, Google-endorsed loyalty signal |
| **No live-blog page type** (no LiveBlogPosting markup anywhere) | New template | Live pages take the "LIVE" Top Stories slot at events |
| **Press releases on the news domain.** Seven `docs/pr-*.html` pages are indexable. All say "Press release." Only two also say "paid" or "sponsored" | `docs/pr-*.html` | Fine at today's volume. A site reputation abuse risk if PR volume grows or drifts off-beat. Paid items must say so plainly, per house rules and Google News policy ([Google News policies](https://support.google.com/news/publisher-center/answer/6204050)). |
| **Publish chain timing.** The sitemap and IndexNow job starts on push, possibly before GitHub Pages finishes deploying. The Meta auto-poster (`social.yml`) runs at :07 and :37 past the hour, so social can lag up to 30 minutes | Workflows | IndexNow may ring before the page is live. A breaking story waits up to half an hour for social. |

**A correction to our own desk manual.** `agents/rapid-response-desk.md` says the first mover takes "roughly 80% of the traffic" and that "publish to indexed: under 5 minutes via IndexNow." The research found no source for the 80% figure. IndexNow does not notify Google: Google tested it in 2021 and has not joined ([Search Engine Roundtable](https://www.seroundtable.com/google-indexnow-32396.html)). IndexNow makes us fast on Bing. Google speed comes from the sitemap, crawlable section pages and earned crawl demand. The desk's "never a second URL" rule is also too strict. Practice varies, and a new URL is right when the story materially changes, such as a verdict, a death or a closed deal ([Lumar](https://www.lumar.io/blog/best-practice/seo-for-news-publisher-websites)). Update the desk file to match.

### The prioritized checklist

"Owner" follows Rule 2: the system does the system's work, and Terry only does what needs his login or his decision. Each fix goes in the template (`wire.py` or the article template), not hand-edited pages. These apply to all five sites, but only the Newswire repo was inspected. Gospel uses `render_site.py`, so the same fixes go there.

| # | Fix | Owner | Cost |
|---|---|---|---|
| 1 | Full timestamps with Pacific offset in schema and news sitemap, plus a visible "Published 2:05 PM PT · Updated 4:40 PM PT" line under the headline. Change `dateModified` only for real updates | Claude | Free |
| 2 | Publisher block with `url`, `logo` and `sameAs` (links to official social profiles). Footer links to About, Masthead, Contact, Corrections, Ethics and a Sponsored Content Policy | Claude builds. Terry approves wording | Free |
| 3 | Named Person bylines with author pages (bio, credentials, photo, social links, ProfilePage markup). Keep "News Desk" only for true desk copy | Terry chooses names and supplies bios. Claude builds | Free |
| 4 | Three image crops (16:9, 4:3, 1:1, at least 1200px wide) made automatically at build time, all listed in the schema, with the license source recorded per house rules | Claude | Free |
| 5 | Preferred Sources button on every article, on every brand's domain (it works per domain or subdomain, not per folder ([arwriterai, secondary](https://arwriterai.com/en/blog/google-preferred-sources-button-publishers-2026/))) | Claude | Free |
| 6 | Chain publishing: wait for the Pages deploy, then sitemap, then IndexNow, then social for breaking items (manual trigger on the poster) | Claude | Free |
| 7 | WebSub `rel="hub"` link in every feed, plus a ping to a public hub on publish | Claude | Free |
| 8 | LiveBlogPosting template (one URL, timestamped updates, start and end times) for awards nights and premieres. Vendors disagree on whether Google approval is needed for the red "LIVE" badge ([Tickaroo](https://tickaroo.com/en/blog/how-to-get-the-red-live-badge-on-google-using-liveblogs)) | Claude | Free |
| 9 | PAID OUT and PR pages: a "Sponsored" or "Paid press release" label on every paid page, kept on our beat. If volume grows, move them to a separate press-release section or noindex them (tell Google not to list them) | Claude flags. Terry decides | Free |
| 10 | SYNDICATED IN copies set to noindex. Google now recommends noindex, not canonical tags, for syndicated copies ([Search Engine Land](https://searchengineland.com/google-no-longer-recommends-canonical-tags-for-syndicated-content-406491)). Our syndication-out agreements should require partners to noindex | Claude, plus contract template | Free |
| 11 | Google Search Console and Bing Webmaster Tools verified on all five domains, with sitemaps submitted | Terry (logins). About 2 minutes each with Bing's import | Free |
| 12 | Per-item image enclosures in feeds (for Apple News, Flipboard, NewsBreak) | Claude | Free |
| 13 | Optional: Cloudflare's free plan in front of GitHub Pages, for custom headers and cache control. This changes DNS (the internet's address book for our domain) | Terry decides | Free tier |

**Do not build:** Google's Indexing API (officially for job postings and livestreams only, and Google treats misuse as a spam signal ([Google](https://developers.google.com/search/apis/indexing-api/v3/using-api); [SER](https://www.seroundtable.com/google-indexing-api-abuse-spammy-low-quality-36919.html))). AMP, a fast-page format that is no longer required for Top Stories ([Google, 2021](https://developers.google.com/search/blog/2021/04/more-details-page-experience)). Sitemap "pings," which Google and Bing switched off ([Google, 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping); [ctrl.blog](https://www.ctrl.blog/entry/sitemap-ping-indexnow/)).

---

## Run the first 15 minutes like a pit crew

### How SEO-led newsrooms are organized

Big newsrooms put audience and SEO editors on the desk who watch search demand constantly. They set Google Trends to a **one-hour window** to spot breakout terms, and they put those exact words in the headline, URL, opening text and description ([WTF is SEO?, search summary](https://www.seoforjournalism.com/p/seo-for-breaking-news)). They publish early, update the same page, open a live blog when people search "live" or "updates," and then build follow-ups (who is, timeline, what we know) linked from the original ([WTF is SEO?](https://www.seoforjournalism.com/p/seo-for-breaking-news); [Press Gazette](https://pressgazette.co.uk/platforms/google-news-seo-tips-publishers/)). **Top Stories visibility lasts from a few hours to about two days** ([Eric Schwartzman / Barry Adams](https://www.ericschwartzman.com/news-seo-barry-adams/)). After that, the follow-up cluster and Discover carry the traffic. No source describes the internal SEO desks at TMZ, Page Six, E!, ET, US Weekly, Variety, Deadline or THR, so this report does not guess at them.

At our size, the "SEO editor" is a checklist and an agent, not a person. The Rapid Response Desk detects the story. Claude drafts the page with all markup complete. **A named human signs off**, which is a house rule. The publish chain does the rest.

### The first 15 minutes

| Minute | Step | Why |
|---|---|---|
| 0 to 2 | Confirm to house standard: a primary source, or a credible outlet credited by name. **Check the embargo field. Embargoes are hard stops** | Accuracy protects topic authority. A wrong scoop costs more than a late one |
| 2 to 4 | Pull the exact search term from Google Trends (one-hour window, "Trending now") | The words people type decide whether you are in the race |
| 4 to 6 | Set the URL slug to that term (it cannot change later without redirects). Write a search headline of about 70 characters or fewer that starts with the name. The on-page H1 can carry more voice, and the social headline matches the facts | Top Stories truncates at about 70 to 80 characters ([SEO for Google News](https://www.seoforgooglenews.com/p/the-5-seo-article-headlines-google)) |
| 6 to 10 | Write a 150 to 250-word brief: what happened, who confirmed it, when, plus a licensed 16:9 image at least 1200px wide with its credit, and full NewsArticle markup with a real timestamp | The house brief length comes from our desk manual. No published source sets a word count |
| 10 to 12 | Named sign-off, then publish | House rule. The system records who signed off |
| 12 to 15 | Confirm the page is live, the sitemap rebuilt and IndexNow accepted. Trigger the social poster by hand. Send a push alert if it is tier one | Makes discovery signals fire within minutes, not on the hourly backup |
| 15 to 90 | Expand on the same URL with context, reaction and original reporting. Update `dateModified` honestly. Open a live blog if searches include "live." Commission two follow-ups and link both ways | Adams: spin off articles through the day, and link to an explainer ([Press Gazette](https://pressgazette.co.uk/platforms/google-news-seo-tips-publishers/)) |

**Pre-writes are the small newsroom's secret weapon.** For every awards show, premiere and verdict date on our Events Calendar, prepare nominee lists, "who is" profiles and winner templates days ahead, as People does ([Built In](https://builtin.com/job/summer-intern-people-editorial/4077696)). On the night, the only work left is filling in a name. This is how a three-person desk can be first.

**Timing for non-breaking work.** Publish breaking news the minute it is confirmed. One October 2026 dataset found that features published 7 am to 1 pm local time get about 12% more Discover traffic, and weekend features about 29% more ([Newsifier](https://www.newsifier.com/publisher-insights/october-2026)). Another guide disagrees ([The Sharp Digital](https://www.thesharpdigital.com/blog/discover-feed-signals-the-complete-2026-guide)). Schedule features for Pacific mornings and weekends, then check our own Search Console Discover data by hour after six weeks. Expect patience. One new publication had **no Top Stories presence for its first eight weeks** ([Search Engine Land, search summary](https://searchengineland.com/news-publication-google-visibility-484268)). That is a single case.

### Tools and prices

| Tool | What it does | Price (as reported) | Verdict for us |
|---|---|---|---|
| Google Trends, Google Alerts, Search Console, competitors' RSS feeds | Demand spotting, monitoring, News and Discover reports | Free | **Core kit. Use now** |
| X Explore, TikTok Creative Center | Social trend spotting | Free | Use now. CrowdTangle closed in Aug 2024, and its replacement excludes commercial newsrooms ([NPR](https://www.npr.org/2024/08/14/nx-s1-5074143/meta-shutters-tool-used-to-fight-disinformation-despite-outcry/page/2)) |
| NewzDash | Tracks Top Stories, Google News and Discover visibility | 14-day free trial. Paid tiers by demo only, price unpublished ([NewzDash](https://www.newzdash.com/guide/best-news-seo-tools-publishers-2026-full-stack)) | **Paid after trial.** Run the trial during a big event week |
| Exploding Topics | Spots rising topics | $39 / $99 / $249 per month ([Market Intelligence Tools](https://marketintelligencetools.com/reports/exploding-topics-pricing/)) | **Paid.** Optional at $39 |
| Glimpse | Google Trends add-on | About $99 to $299 per month (third-party reports) ([OutlierKit](https://outlierkit.com/resources/glimpse-alternatives/)) | Paid. Skip for now |
| BuzzSumo | Content and PR research | $199 to $999 per month ([OutlierKit](https://outlierkit.com/resources/buzzsumo-alternatives/)) | Paid. Useful later for PR STARPOWER |
| Chartbeat / Parse.ly | Real-time newsroom analytics | About $13,000 a year, or from $2,000 a month ([G2](https://www.g2.com/products/chartbeat/pricing); [News Media Help Desk](https://www.newsmediahelpdesk.org/parse-ly-getting-started-guide/)) | Enterprise. Not yet |
| Dataminr / NewsWhip | Breaking-event and social-velocity alerts | About $15,000 to $50,000+ and about $12,000 a year (third-party estimates) ([PR Lab](https://prlab.co/blog/the-best-media-monitoring-tools-for-news-and-social-media/)) | Enterprise. Not yet |

---

## Most distribution doors are shut to small publishers, but five are open

### Aggregators (apps and portals that republish or link to news)

| Channel | Status | What it takes | Cost and money | Fit |
|---|---|---|---|---|
| Google News / Top Stories | **Automatic.** No application since 2019. Publisher Center no longer uses submitted feeds ([Google](https://support.google.com/news/publisher-center/answer/9607025?hl=en); [Google News Help](https://support.google.com/news/publisher-center/answer/15898024)) | Follow the News policies. The Search Console News report shows whether we appear | Free | All news brands |
| **NewsBreak** | **Open** application for US-focused publishers | About page, staff info, bylines, image credits, mostly original content. Then upload RSS ([NewsBreak FAQ](https://support.newsbreak.com/publisher-faq)) | Free. **Read the terms first:** critics say it takes a broad content license and strips publisher ads and calls to action ([Nearview Media](https://nearviewmedia.com/newsbreak/)) | Newswire, HNA, Gospel. World Newswire risks the "US-focused" rejection |
| **SmartNews** | **Open**, selective | A full-text "SmartFormat" feed (an enhanced RSS) that passes their validator ([SmartNews](https://about.smartnews.com/en/press/publishers.html)) | Free. Revenue share not published | Newswire first |
| **Flipboard** | **Open**, human review | Claim a magazine, submit RSS ([PostRSS, secondary](https://postrss.com/can-you-add-an-rss-feed-to-a-flipboard-magazine-whats-actually-possible/)) | Free | All brands |
| **Yahoo Creators** | **Open with waitlist**, as an individual creator | Apply as a creator. Acceptance not guaranteed ([Yahoo Creators FAQ](https://webflow.creators.yahooinc.com/faq)) | **50/50 ad revenue share** | Terry personally |
| Yahoo News syndication | Invite | Direct outreach to partner managers with traffic numbers ([Digiday](https://digiday.com/media/yahoo-takes-cues-from-platforms-as-it-offers-more-editorial-control-to-creators)) | Negotiated | After 90 days of data |
| MSN Partner Hub | **Invite only, possibly paused.** The pause claim comes from an AI-written forum answer ([Microsoft Q&A](https://learn.microsoft.com/en-us/answers/questions/5850858/how-can-i-apply-for-msn-partner-hub-program)) | Request an invite code. Content partners in Microsoft's directory are a workaround ([air.io](https://air.io/en/on-air/how-to-join-msn-to-spread-your-content)) | Free to request | Apply anyway, plan as closed |
| Apple News | Reportedly closed to unsolicited applications since 2025 ([Publisher in a Box](https://publisherinabox.com/apple-news-for-publishers)) | RSS through News Publisher ([Apple](https://support.apple.com/en-gu/guide/news-publisher/apdc2c7520ff/icloud)). Feeds are ready | Free | Apply anyway |
| Perplexity Comet Plus | Program exists. Entry terms for small publishers unclear | Be crawlable and cited | 80% of a $42.5M pool shared by visits and citations. No payouts disclosed ([Keywords Everywhere](https://keywordseverywhere.com/news/perplexity-updates/)) | Watch |

PR STARPOWER is a publicity operation, not an editorial publisher. It is unlikely to qualify for any aggregator, and its home is the paid wires below.

### Press-release wires: what clients pay to reach newsrooms

| Wire | Reported price per US release | Note |
|---|---|---|
| EIN Presswire | From $99.95, packages to $499.95 ([Jerusalem Post](https://www.jpost.com/business-and-innovation/article-898710)) | Budget tier |
| PRWeb | About $120 to $245 ([PR News.io](https://prnews.io/blog/pr-distribution-software.html)) | Budget |
| Newswire.com, eReleases | From about $399 | Mid |
| Business Wire | **$475 starting, 400 words, US** (their own page, seen via snippet) ([presswire.com snippet](https://presswire.com/press-release-distribution-pricing/)) | The only near-verified premium price |
| PR Newswire | About $850 to $1,145 national, plus about $195 a year membership ([Pressonify](https://pressonify.ai/blog/press-release-distribution-pricing-comparison-2026)) | Vendor estimates |
| GlobeNewswire | About $350 to $1,500 ([RhinoRank](https://www.rhinorank.io/blog/press-release-distribution-cost/)) | No public rate card |
| ACCESS Newswire | From about $934 a month subscription ([Jerusalem Post](https://www.jpost.com/business-and-innovation/article-898710)) | Subscription |

Most of these figures come from vendor and affiliate blogs, so treat them as 2026 estimates. Which wires actually reach Google News is a vendor claim, not verified. AP and Reuters offer no public contributor door for small publishers. Reuters Connect lets established news organizations trade content for points ([Digiday](https://digiday.com/media/reuters-building-marketplace-video-hungry-publishers)). For PR STARPOWER, pass wire costs through to clients with a markup, and log them in the Work Ledger.

### Social as search inventory

Social posts now rank in Google on their own. **Since 10 July 2025, Google can index public posts from Instagram professional accounts**, using a toggle under Settings, Privacy, "Allow public photos and videos to appear in search engine results" ([Kapwing](https://www.kapwing.com/resources/instagram-posts-in-google-search-what-creators-need-to-know/)). Discover shows followed creators' X, Instagram and YouTube Shorts posts ([Google](https://blog.google/products-and-platforms/products/search/personalize-search-discover-news/)). YouTube's Top News shelf shows only sources that follow Google News policies and that YouTube deems authoritative ([YouTube Help](https://support.google.com/youtube/answer/9057101?hl=en); [NiemanLab](https://www.niemanlab.org/2023/10/youtube-launches-new-watch-page-that-only-shows-videos-from-authoritative-news-sources/)). Facebook links are nearly dead as a traffic source: **only 1.1% of US Feed views in Q2 2026 were posts with outside links** ([Digiday](https://digiday.com/media/they-hold-us-hostage-publishers-furious-over-terms-change-still-cant-quit-facebook/)). Meta's "Meta One" scheme reportedly caps free link posts for Pages and charges beyond that, with news publishers excluded "for now." That detail comes from a snippet only ([Press Gazette](https://pressgazette.co.uk/platforms/facebook-cash-for-links-scheme-excludes-publishers-for-now/)). Our Meta auto-poster should favor native photo and video posts with the link in the first comment, and we should confirm whether Meta classes our brands as news publishers. The Shade Room shows the payoff of social-first. It grew on Instagram to 500,000 followers before earning money, and reader tips feed its original stories ([Fast Company](https://www.fastcompany.com/90345296/how-the-shade-room-turned-instagram-gossip-into-a-media-empire)). Original stories are exactly what Google's 2026 updates reward.

### Newsletters and push alerts

Preferred Sources and Discover Follow are the free "subscribe" buttons Google built for publishers. Web push alerts (the pop-up notices a reader allows from a browser) are the fastest owned channel. **OneSignal's free plan allows unlimited web push subscribers but sends to only 10,000 per message**. Growth costs $19 a month plus $0.004 per subscriber ([OneSignal](https://onesignal.com/blog/understanding-onesignals-pricing/)). Free until a brand passes 10,000. We found no current pricing for Substack or beehiiv.

---

## Seven ways to lose Google in a week

Each of these has cost real publishers their visibility. **Disguising sponsored content as news**: Google News bans it, and repeated violations remove a site from news features ([Google News policies](https://support.google.com/news/publisher-center/answer/6204050)). **Letting PR or partner content ride the newsroom's authority** at volume, which is site reputation abuse. Penalties have hit CNN, WSJ and Forbes sections ([Search Engine Journal](https://www.searchenginejournal.com/google-strengthens-policy-against-site-reputation-abuse/533018/)). **Mass-producing pages**, AI-written or human, which is scaled content abuse under Google's 2024 spam policies ([Google](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)). **Clickbait and fabricated celebrity headlines**, which the February 2026 Discover update demotes. One analyst estimated flagged sites lost 30 to 60% of Discover traffic ([WrittenlyHub, secondary](https://www.writtenlyhub.com/news/google-discover-core-update-february-2026)). **Faking freshness** by bumping `dateModified` or sitemap dates without a real change. Google stops trusting a site's dates when they do not match reality ([Google, 2023](https://developers.google.com/search/blog/2023/06/sitemaps-lastmod-ping)). **Using the Indexing API for articles**, which Google calls a spam signal. **Buying an expired domain to rank fast**, which is expired domain abuse ([Google](https://developers.google.com/search/blog/2024/03/core-update-spam-policies)). Add an eighth from our own rules: **republishing other outlets' article text**. Google's 2026 core updates moved visibility away from aggregators, and our wire-card rule (their headline, their credited photo, a link out) is the safe line.

Recovery is slow. Google folded its Helpful Content system into core ranking in March 2024, so recovery now waits for core updates ([Amsive](https://www.amsive.com/insights/seo/googles-helpful-content-update-ranking-system-what-happened-and-what-changed-in-2024/)). One publisher describes a three-year, $200,000+ recovery attempt. That is a first-person account and unverified ([Medium](https://medium.com/@lucwiesman/looking-to-recover-from-the-google-helpful-content-update-or-any-algorithm-update-45c25d0d2b62)).

---

## The 30/60/90-day plan, every cost flagged

| Window | Action | Owner | Cost |
|---|---|---|---|
| **Days 1 to 30** | Checklist fixes 1, 2, 4, 5, 6 and 7 on Newswire, then copied to HNA and Gospel | Claude | **Free** |
| | Terry picks bylines and supplies bios. Author pages go live (fix 3) | Terry, then Claude | **Free** |
| | Search Console and Bing Webmaster Tools on all five domains | Terry | **Free** |
| | Correct `agents/rapid-response-desk.md` (the 80% claim, IndexNow and Google, the URL rule) | Claude | **Free** |
| | Label review of all `pr-*` pages. Written sponsored-content policy page | Claude drafts, Terry approves | **Free** |
| | Instagram professional accounts and search indexing on for every brand | Terry (logins) | **Free** |
| | Apply to NewsBreak (after reading the terms), Flipboard and Yahoo Creators. Request an MSN invite and an Apple News channel | Terry (accounts), Claude prepares | **Free** |
| | Pre-write kits for the next three tentpole events on the Events Calendar | Claude and the desk | **Free** |
| **Days 31 to 60** | LiveBlogPosting template, tested live on one event (fix 8) | Claude | **Free** |
| | SmartNews SmartFormat feed, and image enclosures in all feeds | Claude | **Free** |
| | OneSignal web push on Newswire | Claude, Terry signs up | **Free** up to 10,000 per send |
| | NewzDash 14-day trial timed to a big event week | Terry | **Free trial. Paid after, price unpublished** |
| | Optional trend tool | Terry decides | **Paid: Exploding Topics $39/month** |
| | Six-week Search Console review: News appearances, Discover by hour, top entities | Claude | **Free** |
| **Days 61 to 90** | Decide on Cloudflare in front of Pages (fix 13) | Terry | **Free tier** |
| | Pitch Yahoo and MSN partner managers with 60 days of numbers | Claude drafts, Terry sends | **Free** |
| | Decide on PAID OUT placement (same section, separate section or noindex) based on volume | Terry | **Free** |
| | Launch the sellable edition and the audit offer (see "Turning this into money") | Claude builds, Terry sells | **Free to build.** Optional paid storefront |
| | Resell wire distribution to PR STARPOWER clients | Terry | **Paid by the client.** Pass-through: EIN from $99.95, Business Wire from $475 |

**Success at day 90 is not "beating CNN."** Realistic milestones, given the eight-week single case and the small-publisher traffic slide: our stories appearing in the Search Console News report, the first Discover impressions on LA-event stories, at least one aggregator accepted, and at least one other outlet citing a Newswire original. That citation is the topic-authority signal that compounds.

---

## Keeping this playbook current

Google changes the news rules several times a year, so this report is a living document. Give it a dated "last checked" line at the top of every revision.

| How often | What to re-check | Where |
|---|---|---|
| **Weekly (5 minutes)** | Any core, spam or Discover update in progress | Google Search Status Dashboard (status.search.google.com); [Google Search Central blog](https://developers.google.com/search/blog/2026/02/discover-core-update); [Search Engine Roundtable](https://www.seroundtable.com/google-search-traffic-drops-news-publishers-40645.html) |
| **Monthly** | Our News and Discover numbers in Search Console. Whether IndexNow is accepted (Bing Webmaster Tools). The publisher league table. Discover and Top Stories trend analysis | Search Console; Bing Webmaster Tools; [Press Gazette US top 50](https://pressgazette.co.uk/most-popular-websites-news-us-monthly/); [NewzDash guides](https://www.newzdash.com/guide/google-news-optimization-news-seo); [SEO for Google News](https://www.seoforgooglenews.com/p/the-5-seo-article-headlines-google); [WTF is SEO?](https://www.seoforjournalism.com/p/seo-for-breaking-news) |
| **Quarterly** | Google's rulebooks: news sitemaps, Article structured data, byline dates, Discover, Google News policies, spam and site reputation policies, Preferred Sources | [News sitemaps](https://developers.google.com/search/docs/advanced/sitemaps/news-sitemap?hl=en); [Article](https://developers.google.com/search/docs/data-types/article); [Discover](https://developers.google.com/search/docs/appearance/google-discover?authuser=1); [News policies](https://support.google.com/news/publisher-center/answer/6204050); [Preferred Sources](https://developers.google.com/search/docs/appearance/preferred-sources) |
| **Quarterly** | Distribution doors: MSN invite status, Apple News applications, NewsBreak, SmartNews and Yahoo Creators criteria, Meta link rules | [MSN](https://support.microsoft.com/en-us/msn/partner-hub/how-to-set-up-your-msn-partner-hub-account); [Apple](https://support.apple.com/en-gu/guide/news-publisher/apdc2c7520ff/icloud); [NewsBreak](https://publishers.newsbreak.com/); [SmartNews](https://about.smartnews.com/en/press/publishers.html); [Yahoo Creators](https://webflow.creators.yahooinc.com/faq) |
| **Quarterly** | Tool and wire prices; the NewzDash Entertainment Top 100 | Vendor pages; [NewzDash list](https://ww2.newzdash.com/about/all-news-publishers-tracked/U.S./2/Entertainment/) |
| **Yearly** | Reuters Institute Digital News Report (June); Chartbeat's publisher traffic report | [Reuters Institute](https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism); [Axios on Chartbeat](https://www.axios.com/2026/03/17/chartbeat-search-traffic-ai-chatbots?stream=top) |

**Open questions to settle at the next check, once these sites can be read in full.** What the August 2026 site reputation update says. Whether a November 2026 core update exists. The outcome of the EU investigation. Meta One's exact limits. Whether MSN onboarding is paused. LiveBlog badge requirements. Accepted sitemap date formats and logo specifications. GitHub Pages' cache and build limits. The rows of the NewzDash entertainment list.

---

## Turning this into money

Terry's two keys are domination and monetization. This playbook serves both: it helps us dominate niche breaking news, and it is a product in its own right. Small publishers, publicists and churches all face the same 60% search slide and have no in-house SEO editor. **Every price below is an estimate, not market research.** None of the research priced SEO courses or audits. Test each price with five real buyers before printing it.

### Two editions

| Terry's private playbook (keep in-house) | Sellable edition (safe to publish) |
|---|---|
| Our repo audit, file names, workflow timings and IndexNow key setup | The general technical checklist and plain-English explanations |
| Our beat strategy: which LA events, which faith-entertainment lanes, which competitors we target | The "where small sites can win" framework, without our targets |
| Rapid Response Desk internals, source lists, publicist contacts, Events Calendar contact pipeline | The generic "first 15 minutes" routine and pre-write method |
| Our Search Console data, revenue, Work Ledger entries and client names (confidential clients stay in the private Sheet only, per house rules) | Anonymized before-and-after results, with written client permission |
| Partner pitches and negotiated terms with Yahoo, MSN and NewsBreak | The aggregator door table, updated quarterly as a subscriber perk |
| Wire markup and resale margins | The wire price comparison (attributed estimates) |

Two rules keep the sellable edition safe. First, **never promise rankings**. Google decides inclusion and does not guarantee placement, so selling "guaranteed Top Stories" would be misleading. Sell process, fixes and training. Second, **paraphrase and cite**. Do not copy sources' text. The research is cited so buyers can verify it, which is also a selling point.

### Products and estimated prices

| Product | Buyer | Estimated price |
|---|---|---|
| Ebook: *Breaking News, Small Newsroom* (built from this report) | Indie publishers, journalism students, bloggers | **Estimate: $19 to $49** |
| Template pack: schema templates, news-sitemap and IndexNow workflow for static sites, first-15-minutes card, pre-write kits, sponsored-label policy | Small publishers, developers | **Estimate: $49 to $149** |
| Self-paced video course (6 to 8 short lessons) | Publishers, publicists | **Estimate: $199 to $499** |
| Newsroom-SEO audit: checklist review of a site, a written report and a 30/60/90 plan | Independent and local publishers | **Estimate: $750 to $2,500** per site |
| Church and ministry media audit: news pages, events, YouTube, Preferred Sources, Instagram search | Churches, gospel labels, faith ministries | **Estimate: $500 to $1,500** |
| Publicist workshop: "How Google picks the story, and how to pitch outlets that rank" | PR firms, publicists, talent managers | **Estimate: $99 to $299 per seat, or $1,500 to $5,000 private** |
| Done-for-you setup: we install the static-site news stack | Small publishers | **Estimate: $1,500 to $5,000** |
| Monthly retainer: quarterly re-check, update alerts, one audit refresh | Past audit clients | **Estimate: $300 to $1,500 per month** |
| PR STARPOWER distribution package: release writing, wire placement at cost plus markup, our sites (labeled sponsored), and a client report with a market-value sidebar | Artists, events, brands | **Estimate: $500 to $2,500** plus wire pass-through |

The free layer sells the paid layer. A short free checklist on Newswire's own site, signed with Terry's credentials, builds an email list and showcases our expertise. Every sale and audit gets a Work Ledger line with date, client, hours and market value, per the standing rule. Every client gets a report and a receipt. The PR STARPOWER package must stay clearly labeled sponsored on our news sites, and kept on our beat, so the money never puts the newsroom's Google standing at risk.

---

## Conclusion

The research changes the question. "How do we get to the top of Google in minutes" assumed a speed race that only a handful of trusted brands can run, because Google's speed for them comes from years of crawl trust, not a button. The real opening for a small newsroom in late 2026 is that Google is actively demoting the giants' weaknesses: aggregation, clickbait, distance from the story and sponsored sections riding news authority. It is rewarding what an LA-based, credentialed, faith-and-entertainment wire can be: local, original, specialist and transparent. Our strongest asset is not IndexNow but the Events Calendar and red-carpet access, because original reporting that other outlets cite is the one signal no amount of money can buy.

The biggest risk is internal, not Google. A publisher that also runs PR and paid distribution sits in the exact category Google's site reputation policy targets. The labeling and placement discipline in this plan is what protects the newsroom's search standing, and with it the revenue businesses that depend on it. Build the trust first, keep the money clearly labeled, and the playbook pays twice: once in traffic, and again as a product.
