"""
urls.py additions — wire up sitemap.xml, robots.txt, and llms.txt.

Add these imports and url patterns to your ROOT urls.py.
"""

from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sitemaps.views import sitemap
from django.shortcuts import render
from django.urls import path

from .sitemaps import sitemaps  # adjust import path to where sitemaps.py lives


def robots_txt(request):
    return render(
        request, "robots.txt",
        {"site": get_current_site(request)},
        content_type="text/plain",
    )


def llms_txt(request):
    return render(
        request, "llms.txt",
        {"site": get_current_site(request)},
        content_type="text/plain",
    )


urlpatterns = [
    # ... your existing patterns ...
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("llms.txt", llms_txt, name="llms_txt"),
]
