from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import include, path

from .sitemaps import sitemaps


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
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps},
         name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("llms.txt", llms_txt, name="llms_txt"),
    path("", include("core.urls")),
]
