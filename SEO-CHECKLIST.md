# SEO Submission & Best-Practices Checklist

A repeatable checklist for getting every site indexed by **Bing** and **Yandex**
(and well-positioned in search generally). Work top to bottom for each new site.

---

## 1. Submit & Verify the Site

### Bing — [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ ] Sign in (Microsoft / Google / Facebook account).
- [ ] Add the site — **fastest path: import from Google Search Console** (pulls sites + sitemaps in one click).
- [ ] Verify ownership (pick one):
  - [ ] **DNS CNAME** — best for managing many sites/subdomains at once.
  - [ ] **Meta tag** — `<meta name="msvalidate.01" content="YOUR_CODE">` in homepage `<head>`.
  - [ ] **XML file** — upload `BingSiteAuth.xml` to site root.
- [ ] Submit sitemap under **Sitemaps** (e.g. `https://example.com/sitemap.xml`).
- [ ] Enable **IndexNow** for instant URL submission (see `indexnow/`).

### Yandex — [Yandex Webmaster](https://webmaster.yandex.com)
- [ ] Create a Yandex account and add the site.
- [ ] Verify ownership (pick one):
  - [ ] **DNS TXT record**.
  - [ ] **Meta tag** — `<meta name="yandex-verification" content="YOUR_CODE">`.
  - [ ] **HTML file** upload to root.
- [ ] Submit sitemap under **Indexing → Sitemap files**.
- [ ] Set **region** and **site language** (Yandex is strongly geo/locale-aware).
- [ ] Use **Reindex pages** to request crawling of priority URLs.

---

## 2. Technical Foundations (do these once per site)

- [ ] **HTTPS** enabled and forced (HTTP → HTTPS redirect).
- [ ] `robots.txt` present at root and not blocking important pages (template in `templates/`).
- [ ] Valid **XML sitemap**, referenced from `robots.txt` (template in `templates/`).
- [ ] No accidental `noindex` on pages you want ranked.
- [ ] **Canonical tags** (`<link rel="canonical">`) to consolidate duplicates.
- [ ] **Mobile-friendly / responsive** layout.
- [ ] Good **page speed / Core Web Vitals** (LCP, CLS, INP).
- [ ] Logical **internal linking** — no orphan pages.
- [ ] **Structured data** (Schema.org JSON-LD) where relevant.

---

## 3. On-Page SEO (per page)

- [ ] Unique, descriptive `<title>` (keep the primary keyword near the front — Bing weights exact match).
- [ ] Compelling `<meta name="description">`.
- [ ] Exactly one `<h1>`; logical `<h2>`/`<h3>` hierarchy.
- [ ] Descriptive `alt` text on images.
- [ ] Original, in-depth content matched to search intent (no thin/duplicate pages).
- [ ] Clean, readable URLs.

---

## 4. Engine-Specific Notes

### Bing leans on
- Exact-match keywords in titles/headings/domain (more than Google).
- Social signals (shares, mentions).
- Clean crawlable HTML; established domain authority.
- Well-optimized multimedia (images/video).
- **IndexNow** (Bing co-created it).

### Yandex leans on
- **Behavioral signals** — CTR, dwell time, bounce (via Yandex Metrica). Real engagement matters most here.
- Correct **region + language**; Russian-language content favored for RU results.
- **ICS / Site Quality Index** — holistic quality score.
- **Commercial factors** for e-commerce (contact info, pricing, assortment, delivery).
- **Turbo Pages** for fast mobile.
- Strict anti-spam: avoid link schemes (Minusinsk) and keyword-stuffed/over-optimized text (Baden-Baden).

---

## 5. Ongoing

- [ ] Ping **IndexNow** on every publish/update (`indexnow/submit.sh`).
- [ ] Re-submit sitemap after major content changes.
- [ ] Monitor crawl errors, index coverage, and search reports in both consoles.
- [ ] Keep an eye on Core Web Vitals and fix regressions.
