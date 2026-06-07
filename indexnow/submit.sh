#!/usr/bin/env bash
#
# submit.sh — push URLs to IndexNow so Bing & Yandex (and others) crawl them fast.
#
# One API key works across all IndexNow-enabled engines. Submitting to a single
# endpoint propagates to the rest, so we just POST to the IndexNow API.
#
# Setup (once per site):
#   1. Generate a key:                ./submit.sh --genkey
#   2. Host the key file at site root: https://example.com/<key>.txt
#      (the file's contents = the key itself; a key.txt is created for you)
#   3. Submit URLs:                    ./submit.sh https://example.com/page1 https://example.com/page2
#      or from a file (one URL/line):  ./submit.sh --file urls.txt
#
# Config: set HOST and KEY below, or pass via env vars INDEXNOW_HOST / INDEXNOW_KEY.

set -euo pipefail

HOST="${INDEXNOW_HOST:-example.com}"          # your domain, no scheme
KEY="${INDEXNOW_KEY:-}"                        # your IndexNow key (32+ hex chars)
ENDPOINT="https://api.indexnow.org/indexnow"  # shared endpoint; fans out to Bing/Yandex/etc.

err() { echo "Error: $*" >&2; exit 1; }

# --- generate a key + key file ---------------------------------------------
if [[ "${1:-}" == "--genkey" ]]; then
  newkey="$(LC_ALL=C tr -dc 'a-f0-9' </dev/urandom | head -c 32)"
  echo -n "$newkey" > "${newkey}.txt"
  echo "Generated key: $newkey"
  echo "Created file:  ${newkey}.txt"
  echo "Upload it to:  https://${HOST}/${newkey}.txt"
  echo "Then run:      INDEXNOW_KEY=${newkey} ./submit.sh <urls...>"
  exit 0
fi

[[ -n "$KEY" ]] || err "No key set. Run './submit.sh --genkey' or export INDEXNOW_KEY."
[[ "$HOST" != "example.com" ]] || err "Set HOST (edit script or export INDEXNOW_HOST)."

# --- collect URLs -----------------------------------------------------------
urls=()
if [[ "${1:-}" == "--file" ]]; then
  [[ -n "${2:-}" && -f "$2" ]] || err "Usage: ./submit.sh --file <path>"
  while IFS= read -r line; do
    [[ -n "$line" && "$line" != \#* ]] && urls+=("$line")
  done < "$2"
else
  urls=("$@")
fi

[[ ${#urls[@]} -gt 0 ]] || err "No URLs provided. Usage: ./submit.sh <url> [url...] | --file <path>"

# --- build JSON payload -----------------------------------------------------
url_json=""
for u in "${urls[@]}"; do
  url_json+="\"${u}\","
done
url_json="[${url_json%,}]"

payload=$(cat <<JSON
{
  "host": "${HOST}",
  "key": "${KEY}",
  "keyLocation": "https://${HOST}/${KEY}.txt",
  "urlList": ${url_json}
}
JSON
)

echo "Submitting ${#urls[@]} URL(s) to IndexNow for ${HOST}..."
http_code=$(curl -sS -o /tmp/indexnow_resp -w "%{http_code}" \
  -X POST "$ENDPOINT" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$payload")

case "$http_code" in
  200|202) echo "OK ($http_code) — URLs accepted." ;;
  400) err "400 Bad request — check JSON / URL format." ;;
  403) err "403 Forbidden — key file not found or invalid at https://${HOST}/${KEY}.txt." ;;
  422) err "422 — URLs don't match the host, or key mismatch." ;;
  429) err "429 — too many requests; slow down." ;;
  *)   err "Unexpected response $http_code: $(cat /tmp/indexnow_resp)" ;;
esac
