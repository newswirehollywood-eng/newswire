# World Newswire Press

**worldnewswirepress.com** — a global newsroom and wire service. Giving the world a voice.

Part of the Newswire Hollywood media group. Editor: Terry Bryant.

## How it works, in one paragraph

GitHub Pages serves the `docs/` folder as the website. Every hour a free GitHub
Action runs `wire.py`, which reads 36 public RSS feeds from the world's
newsrooms (`data/feeds.json`), sorts the headlines into five regions and three
topics, puts our own signed-off stories (`data/originated.json`) on top, and
rewrites the homepage and section pages. A second Action runs `sitemaps.py`
so search engines always have an up-to-date map, and pings IndexNow.

## Files

| Path | What it is | What breaks without it |
|---|---|---|
| `wire.py` | The publishing engine | The site never updates |
| `sitemaps.py` | Writes sitemap.xml and news-sitemap.xml | Google and Bing find new stories slowly |
| `data/feeds.json` | The newsrooms we follow | The wire is empty |
| `data/originated.json` | Our own stories and releases, with sign-off and embargo | Our stories vanish from every index page |
| `data/image-credits.json` | License record for every image we host | We cannot prove image rights |
| `docs/` | The website itself | No website |
| `drafts/` | Article pages waiting for sign-off or embargo | (Created when needed) |
| `.github/workflows/` | The hourly automations | Nothing runs on its own |
| `runbook/` | Launch steps, feed checks, learning log | Terry loses the how-to |

## Run it by hand

```
python3 wire.py --offline   # rebuild pages without fetching feeds
python3 wire.py             # full run
python3 sitemaps.py         # rebuild sitemaps
```

Zero cost: standard-library Python only, free Actions minutes on a public repo.
