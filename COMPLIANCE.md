# SEO Standard — Compliance Tracker

Standard defined in `django-standard/`. A site is **compliant** when all four
boxes are checked. Add a row per site.

Each site needs:
- **sitemap** — `/sitemap.xml` served by Django **with `<lastmod>`** on every URL
- **robots** — `/robots.txt` served, `Sitemap:` line present
- **llms** — `/llms.txt` served at root
- **submitted** — sitemap URL submitted in Bing **and** Yandex

| Site | sitemap+lastmod | robots | llms | submitted (Bing/Yandex) | Notes |
|---|:---:|:---:|:---:|:---:|---|
| wedraftit.ca | ☐ | ☑ | ☑ | ☐ | Sitemap exists but **missing `<lastmod>`** — apply standard |
| _add site_ | ☐ | ☐ | ☐ | ☐ | |
| _add site_ | ☐ | ☐ | ☐ | ☐ | |

> Note for wedraftit.ca: robots.txt already references sitemap + llms, and
> llms.txt exists — only the sitemap needs `<lastmod>` added per the standard.
