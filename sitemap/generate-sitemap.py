#!/usr/bin/env python3
"""
generate-sitemap.py — build sitemap.xml for one or many sites, no manual page lists.

For each site it will:
  1. Check if a sitemap already exists (/sitemap.xml, /sitemap_index.xml). If so,
     it tells you to just submit that URL — nothing to build.
  2. Otherwise crawl the site (same-domain links only) and write a sitemap.xml.

Usage:
  ./generate-sitemap.py https://example.com
  ./generate-sitemap.py --file sites.txt              # one URL per line
  ./generate-sitemap.py https://a.com https://b.com --max 500 --out ./out

Output: ./out/<domain>-sitemap.xml  (plus a console summary per site)

Stdlib only — no pip install needed. Python 3.8+.
"""

import argparse
import sys
import time
import os
import urllib.request
import urllib.error
from urllib.parse import urljoin, urldefrag, urlparse
from html.parser import HTMLParser
from collections import deque
from datetime import date

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

SKIP_EXT = {".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico",
            ".css", ".js", ".pdf", ".zip", ".mp4", ".mp3", ".woff",
            ".woff2", ".ttf", ".xml", ".json", ".rss"}


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "a" and d.get("href"):
            self.links.append(d["href"])
        if tag == "meta" and d.get("name", "").lower() == "robots":
            if "noindex" in d.get("content", "").lower():
                self.noindex = True


def fetch(url, timeout=15):
    """Return (status, content_type, body_text) or (None, None, None) on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ctype = r.headers.get("Content-Type", "")
            body = b""
            if "html" in ctype or "xml" in ctype or ctype == "":
                body = r.read(2_000_000)  # cap at ~2MB
            return r.status, ctype, body.decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, None, None
    except Exception:
        return None, None, None


def existing_sitemap(base):
    """Return URL of an existing sitemap if one is reachable, else None."""
    for path in ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml"):
        url = urljoin(base, path)
        status, ctype, body = fetch(url)
        if status == 200 and body and "<" in body and ("urlset" in body or "sitemapindex" in body):
            return url
    return None


def crawl(start, max_pages):
    """BFS crawl of same-domain HTML pages. Returns a sorted list of URLs."""
    start = start.rstrip("/") + "/"
    host = urlparse(start).netloc
    seen, found = set(), []
    q = deque([start])
    seen.add(start)

    while q and len(found) < max_pages:
        url = q.popleft()
        status, ctype, body = fetch(url)
        if status != 200 or not body or "html" not in (ctype or ""):
            continue

        p = LinkParser()
        try:
            p.feed(body)
        except Exception:
            pass
        if p.noindex:
            continue  # respect noindex — don't list it

        found.append(url)

        for href in p.links:
            nxt, _ = urldefrag(urljoin(url, href))
            pr = urlparse(nxt)
            if pr.scheme not in ("http", "https"):
                continue
            if pr.netloc != host:
                continue
            ext = os.path.splitext(pr.path)[1].lower()
            if ext in SKIP_EXT:
                continue
            if nxt not in seen:
                seen.add(nxt)
                q.append(nxt)
        time.sleep(0.2)  # be polite

    return sorted(set(found))


def write_sitemap(urls, out_path):
    today = date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        lines.append(f"    <lastmod>{today}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def domain_slug(url):
    return urlparse(url).netloc.replace(":", "_") or "site"


def main():
    ap = argparse.ArgumentParser(description="Generate sitemap.xml for one or many sites.")
    ap.add_argument("urls", nargs="*", help="Site root URLs (https://example.com)")
    ap.add_argument("--file", help="File with one site URL per line ('#' comments ok)")
    ap.add_argument("--max", type=int, default=2000, help="Max pages per site (default 2000)")
    ap.add_argument("--out", default="out", help="Output directory (default ./out)")
    args = ap.parse_args()

    sites = list(args.urls)
    if args.file:
        with open(args.file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    sites.append(line)

    if not sites:
        ap.error("No sites given. Pass URLs or --file sites.txt")

    os.makedirs(args.out, exist_ok=True)
    print(f"Processing {len(sites)} site(s)...\n")

    for site in sites:
        if not site.startswith(("http://", "https://")):
            site = "https://" + site
        print(f"=== {site} ===")

        existing = existing_sitemap(site)
        if existing:
            print(f"  ✓ Sitemap already exists: {existing}")
            print(f"    → Just submit this URL in Bing/Yandex. Nothing to build.\n")
            continue

        print("  No existing sitemap found — crawling...")
        urls = crawl(site, args.max)
        if not urls:
            print("  ⚠ Could not crawl any pages (site may block bots, or is JS-only).")
            print("    Try from a machine that can reach the site, or use a hosted")
            print("    generator. See README.\n")
            continue

        out_file = os.path.join(args.out, f"{domain_slug(site)}-sitemap.xml")
        write_sitemap(urls, out_file)
        print(f"  ✓ {len(urls)} pages → {out_file}")
        print(f"    → Upload to {site.rstrip('/')}/sitemap.xml, then submit that URL.\n")


if __name__ == "__main__":
    main()
