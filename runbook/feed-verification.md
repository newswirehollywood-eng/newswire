# Feed verification

Plain English: these are the 36 public RSS feeds wire.py reads. They were
chosen from each outlet's published feed addresses, but they could NOT be
tested when the site was built, because the build sandbox cannot reach those
websites. That is expected. The first real check happens on GitHub's servers
the first time the Wire workflow runs.

After that run, open runbook/wire-feed-status.md: it lists every feed as ok or
dropped (with the reason) and is rewritten every hour. Change each row below
from "unverified" to "ok" or "dropped", and replace or delete dropped feeds in
data/feeds.json. A dropped feed never breaks the site: its cards simply do not
appear.

| Feed | Section | URL | Status |
|---|---|---|---|
| BBC News: World | world | https://feeds.bbci.co.uk/news/world/rss.xml | unverified |
| BBC News: US & Canada | americas | https://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml | unverified |
| BBC News: Latin America | americas | https://feeds.bbci.co.uk/news/world/latin_america/rss.xml | unverified |
| BBC News: Europe | europe | https://feeds.bbci.co.uk/news/world/europe/rss.xml | unverified |
| BBC News: Africa | africa | https://feeds.bbci.co.uk/news/world/africa/rss.xml | unverified |
| BBC News: Middle East | middle-east | https://feeds.bbci.co.uk/news/world/middle_east/rss.xml | unverified |
| BBC News: Asia | asia-pacific | https://feeds.bbci.co.uk/news/world/asia/rss.xml | unverified |
| BBC News: Business | business | https://feeds.bbci.co.uk/news/business/rss.xml | unverified |
| BBC News: Entertainment & Arts | entertainment | https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml | unverified |
| Al Jazeera | world | https://www.aljazeera.com/xml/rss/all.xml | unverified |
| The Guardian: World | world | https://www.theguardian.com/world/rss | unverified |
| The Guardian: Americas | americas | https://www.theguardian.com/world/americas/rss | unverified |
| The Guardian: Africa | africa | https://www.theguardian.com/world/africa/rss | unverified |
| The Guardian: Middle East | middle-east | https://www.theguardian.com/world/middleeast/rss | unverified |
| The Guardian: Asia-Pacific | asia-pacific | https://www.theguardian.com/world/asia-pacific/rss | unverified |
| NPR: World | world | https://feeds.npr.org/1004/rss.xml | unverified |
| DW: Top Stories | world | https://rss.dw.com/rdf/rss-en-top | unverified |
| DW: Business | business | https://rss.dw.com/rdf/rss-en-bus | unverified |
| France 24: World | world | https://www.france24.com/en/rss | unverified |
| France 24: Africa | africa | https://www.france24.com/en/africa/rss | unverified |
| France 24: Middle East | middle-east | https://www.france24.com/en/middle-east/rss | unverified |
| CBC News: World | world | https://www.cbc.ca/webfeed/rss/rss-world | unverified |
| Euronews | europe | https://www.euronews.com/rss?level=theme&name=news | unverified |
| Africanews | africa | https://www.africanews.com/feed/rss | unverified |
| ABC News (Australia) | asia-pacific | https://www.abc.net.au/news/feed/51120/rss.xml | unverified |
| South China Morning Post: World | world | https://www.scmp.com/rss/91/feed | unverified |
| South China Morning Post: Asia | asia-pacific | https://www.scmp.com/rss/3/feed | unverified |
| The Times of India: World | world | https://timesofindia.indiatimes.com/rssfeeds/296589292.cms | unverified |
| The Times of India: Top Stories | asia-pacific | https://timesofindia.indiatimes.com/rssfeedstopstories.cms | unverified |
| The Japan Times | asia-pacific | https://www.japantimes.co.jp/feed/ | unverified |
| CNBC: World Markets | business | https://www.cnbc.com/id/100727362/device/rss/rss.html | unverified |
| Variety | entertainment | https://variety.com/feed/ | unverified |
| Deadline | entertainment | https://deadline.com/feed/ | unverified |
| Religion News Service | faith-culture | https://religionnews.com/feed/ | unverified |
| Christianity Today | faith-culture | https://www.christianitytoday.com/feed/ | unverified |
| Vatican News | faith-culture | https://www.vaticannews.va/en.rss.xml | unverified |
