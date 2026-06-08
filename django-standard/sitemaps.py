"""
sitemaps.py — STANDARD Django sitemap with lastmod for every site.

Drop this into each Django project (adjust url names / models), wire it up in
urls.py (see urls_snippet.py), and add 'django.contrib.sitemaps' to
INSTALLED_APPS (see settings_snippet.py).

Why this file exists: the old sitemaps had <priority>/<changefreq> but no
<lastmod>. Search engines (Bing especially) largely IGNORE priority/changefreq
but DO use <lastmod> to decide what to re-crawl. This standard always emits an
honest <lastmod>.

----------------------------------------------------------------------------
CHOOSING A lastmod SOURCE  (honesty matters — Bing distrusts sitemaps whose
lastmod is always "today" / identical across all URLs):

  * Dynamic content (blog posts, listings, profiles):
        lastmod = the model's `updated_at` field.  <-- gold standard, automatic
  * Static marketing pages (home/about/contact):
        maintain a small PAGE_LASTMOD dict and bump the date when you edit a
        page. Honest, zero infra, survives redeploys (unlike file mtime, which
        resets to "now" on every fresh checkout — do NOT use mtime).
----------------------------------------------------------------------------
"""

from datetime import date

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


# --- Static pages -----------------------------------------------------------
# Map each named URL to the date its content last meaningfully changed.
# Bump the date ONLY when you actually change the page's content.
PAGE_LASTMOD = {
    "home":     date(2026, 6, 8),
    "about":    date(2026, 6, 8),
    "drafters": date(2026, 6, 8),
    "contact":  date(2026, 6, 8),
}


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return list(PAGE_LASTMOD.keys())

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return PAGE_LASTMOD[item]


# --- Dynamic content (example) ---------------------------------------------
# Uncomment and adapt for any model with an `updated_at` (or similar) field.
# This gives fully automatic, always-honest lastmod values.
#
# from myapp.models import Article
#
# class ArticleSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.7
#     protocol = "https"
#
#     def items(self):
#         return Article.objects.filter(published=True)
#
#     def lastmod(self, obj):
#         return obj.updated_at          # DateTimeField/DateField on the model
#
#     # location() is inferred from the model's get_absolute_url()


# Registry passed to the sitemap() view in urls.py.
sitemaps = {
    "static": StaticViewSitemap(),
    # "articles": ArticleSitemap(),
}
