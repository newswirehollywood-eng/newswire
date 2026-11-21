# Launch steps: putting worldnewswirepress.com live

Plain English: the code is finished and in the repo. These are the few switches
only an account owner can flip. Do them in order. Each takes a minute or two.

## 0. Give Claude access to the repo (if not done yet)

Install the Claude GitHub App on the `worldnewswirepress` organization:
https://github.com/apps/claude/installations/select_target
Pick `worldnewswirepress/worldnewswirepress`. Until this is done, Claude saves
the work to a backup branch (`wnp-site-backup`) in the newswire repo instead.

## 1. Turn on GitHub Pages

Repo `worldnewswirepress/worldnewswirepress` > **Settings** > **Pages**
- Source: **Deploy from a branch**
- Branch: **main**, folder: **/docs** > **Save**
- Custom domain: `worldnewswirepress.com` > **Save** (the docs/CNAME file already says this)
- Tick **Enforce HTTPS** once it becomes clickable (can take up to an hour after DNS works)

## 2. Let the automations save their work

Repo > **Settings** > **Actions** > **General** > **Workflow permissions**
- Choose **Read and write permissions** > **Save**

Without this the hourly rebuild runs but cannot save, and the site freezes.

## 3. Point the domain at GitHub (GoDaddy)

GoDaddy > My Products > worldnewswirepress.com > **DNS** > **Manage DNS**.
Delete any existing A record for `@` and any "Parked" or "Forwarding" entry, then add:

| Type | Name | Value | TTL |
|---|---|---|---|
| A | @ | 185.199.108.153 | 1 hour |
| A | @ | 185.199.109.153 | 1 hour |
| A | @ | 185.199.110.153 | 1 hour |
| A | @ | 185.199.111.153 | 1 hour |
| CNAME | www | worldnewswirepress.github.io | 1 hour |

DNS changes usually show within an hour, sometimes up to 48.

## 4. Start the wire

Repo > **Actions** > **Wire** > **Run workflow**. Then **Sitemaps and IndexNow** > **Run workflow**.
After that both run on their own every hour.

## 5. Check it

- https://worldnewswirepress.com loads with the padlock (HTTPS)
- The wire shows live headlines (or the "refreshing" note if a feed is down)
- runbook/wire-feed-status.md lists which feeds answered
- Submit https://worldnewswirepress.com/sitemap.xml and /news-sitemap.xml in
  Google Search Console and Bing Webmaster Tools (free accounts)
