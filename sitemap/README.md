# Sitemaps — build & submit for all sites at once

Bing (and Yandex) want an XML sitemap so they know which pages to crawl. You
rarely need to write one by hand. Three paths, easiest first:

## Path A — You probably already have one (check first!)

Most site builders auto-generate a sitemap. Open these in your browser:

- `https://yoursite.com/sitemap.xml`
- `https://yoursite.com/sitemap_index.xml`

| Platform | Sitemap URL |
|---|---|
| WordPress (5.5+) | `/sitemap.xml` or `/wp-sitemap.xml` (Yoast/RankMath: `/sitemap_index.xml`) |
| Shopify | `/sitemap.xml` |
| Squarespace | `/sitemap.xml` |
| Wix | `/sitemap.xml` |
| Webflow | `/sitemap.xml` (enable in Site Settings → SEO) |
| Ghost | `/sitemap.xml` |

If one loads, **just paste that URL into Bing's "Submit Sitemap" box.** Done —
nothing to build. Do this for each site.

## Path B — Generate one by crawling (no manual page lists)

For sites that *don't* expose a sitemap, `generate-sitemap.py` crawls the live
site and writes the XML for you. It handles many sites in one run.

```bash
cd sitemap

# Single site
./generate-sitemap.py https://example.com

# Many sites at once — list them in sites.txt, then:
./generate-sitemap.py --file sites.txt

# Options
./generate-sitemap.py --file sites.txt --max 500 --out ./out
```

For each site it first checks for an existing sitemap (Path A) and only crawls
if none is found. Output lands in `./out/<domain>-sitemap.xml`.

Then for each generated file:
1. Upload it to the site root as `sitemap.xml`
   (e.g. `https://example.com/sitemap.xml`).
2. Add `Sitemap: https://example.com/sitemap.xml` to the site's `robots.txt`.
3. Submit that URL in Bing Webmaster Tools and Yandex Webmaster.

> Requires Python 3.8+. Stdlib only — no `pip install`. Uses a real browser
> user-agent so most CDNs won't block it. Note: JavaScript-only sites (content
> rendered client-side) may yield few pages — those builders almost always
> provide a native sitemap, so use Path A.

## Path C — Skip the file entirely with IndexNow

Sitemaps tell engines what *exists*; **IndexNow** tells them what *just
changed* and is faster for ongoing updates. They complement each other. See
`../indexnow/`. A sitemap is still worth submitting once for full coverage.

---

### Keeping sitemaps fresh

- Builder-generated sitemaps (Path A) update themselves — set and forget.
- Crawler-generated sitemaps (Path B) are a snapshot; re-run the script after
  adding pages, or wire it into a scheduled job / deploy step.
