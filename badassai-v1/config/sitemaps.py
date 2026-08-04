"""Sitemap per the repo's django-standard: honest <lastmod> for every URL."""

from datetime import date

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

# Bump a date ONLY when that page's content meaningfully changes.
PAGE_LASTMOD = {
    "home": date(2026, 8, 4),
    "about": date(2026, 8, 4),
    "services": date(2026, 8, 4),
    "members": date(2026, 8, 4),
    "newsletter": date(2026, 8, 4),
    "contact": date(2026, 8, 4),
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
        if item == "services":
            # Services render from the database — use the latest edit there.
            from core.models import Service

            latest = (
                Service.objects.filter(active=True)
                .order_by("-updated_at")
                .values_list("updated_at", flat=True)
                .first()
            )
            if latest:
                return latest.date()
        return PAGE_LASTMOD[item]


sitemaps = {
    "static": StaticViewSitemap(),
}
