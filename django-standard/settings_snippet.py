"""
settings.py additions for the SEO standard.

The sitemap framework needs django.contrib.sites to build absolute <loc> URLs,
and django.contrib.sitemaps for the sitemap view.
"""

INSTALLED_APPS = [
    # ... your existing apps ...
    "django.contrib.sites",      # required: provides the domain for <loc>
    "django.contrib.sitemaps",   # required: the sitemap view
]

SITE_ID = 1

# IMPORTANT: set the Site's domain to the REAL domain for each project, or the
# sitemap will emit example.com URLs. Do it once per site, e.g. in a data
# migration or the Django admin (Sites section):
#
#   from django.contrib.sites.models import Site
#   Site.objects.update_or_create(
#       id=1, defaults={"domain": "wedraftit.ca", "name": "We Draft It"}
#   )
