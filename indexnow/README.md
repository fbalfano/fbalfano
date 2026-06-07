# IndexNow — instant indexing for Bing & Yandex

[IndexNow](https://www.indexnow.org/) lets you notify search engines the moment
a page is added, updated, or deleted, instead of waiting for the next crawl.
**One key and one POST** reach Bing, Yandex, Seznam, Naver, and others — they
share submissions with each other.

## Quick start

```bash
cd indexnow

# 1. Generate a key (creates <key>.txt)
./submit.sh --genkey

# 2. Upload the generated <key>.txt to your site root so it's reachable at:
#    https://example.com/<key>.txt
#    (contents of the file must be exactly the key)

# 3. Submit URLs (set your host + key via env or edit the script)
INDEXNOW_HOST=example.com INDEXNOW_KEY=<key> ./submit.sh \
  https://example.com/new-page https://example.com/updated-page

# ...or from a file (one URL per line; '#' lines ignored)
INDEXNOW_HOST=example.com INDEXNOW_KEY=<key> ./submit.sh --file urls.txt
```

## How it works

- The **key file** at your domain root proves you own the site.
- You POST a JSON body (`host`, `key`, `keyLocation`, `urlList`) to
  `https://api.indexnow.org/indexnow`.
- That single endpoint fans the submission out to all participating engines.

## Notes & limits

- URLs must belong to the `host` you declare (no cross-domain submissions).
- Submit **changed** URLs only — don't re-submit your whole site repeatedly.
- Bing also accepts IndexNow via Bing Webmaster Tools; Yandex via Yandex Webmaster.
- Keep the key file in place permanently; deleting it breaks verification.

## Automating per site

Wire `submit.sh` into your publish/deploy step (CI job, post-build hook, or CMS
webhook) so every changed URL is pushed automatically. Store `INDEXNOW_KEY` as a
secret and pass `INDEXNOW_HOST` per site.
