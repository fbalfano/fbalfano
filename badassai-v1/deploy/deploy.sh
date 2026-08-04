#!/usr/bin/env bash
# =============================================================================
# badassai.ca one-shot deploy / update script (Ubuntu/Debian, run as root)
#
# First run:   bash deploy.sh          (installs everything, prompts for config)
# Updates:     bash deploy.sh          (pulls, migrates, collects static, restarts)
#
# Assumes Cloudflare already points badassai.ca at this server.
# =============================================================================
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/fbalfano/fbalfano.git}"
REPO_BRANCH="${REPO_BRANCH:-claude/ai-coaching-domain-choice-olsjtu}"
APP_ROOT=/srv/badassai
APP_DIR="$APP_ROOT/badassai-v1"
ENV_FILE=/etc/badassai.env
SERVICE=badassai
PORT=8001

echo "==> Packages"
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip git nginx >/dev/null

echo "==> Code"
if [ -d "$APP_ROOT/.git" ]; then
    git -C "$APP_ROOT" fetch origin "$REPO_BRANCH"
    git -C "$APP_ROOT" checkout "$REPO_BRANCH"
    git -C "$APP_ROOT" pull origin "$REPO_BRANCH"
else
    git clone --branch "$REPO_BRANCH" "$REPO_URL" "$APP_ROOT"
fi

echo "==> Virtualenv"
[ -d "$APP_DIR/venv" ] || python3 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install -q -r "$APP_DIR/requirements.txt"

if [ ! -f "$ENV_FILE" ]; then
    echo "==> Environment ($ENV_FILE)"
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    read -r -s -p "Migadu password for hello@badassai.ca: " SMTP_PASS; echo
    cat > "$ENV_FILE" <<ENV
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=badassai.ca,www.badassai.ca
EMAIL_HOST=smtp.migadu.com
EMAIL_PORT=465
EMAIL_USE_SSL=1
EMAIL_HOST_USER=hello@badassai.ca
EMAIL_HOST_PASSWORD=$SMTP_PASS
DEFAULT_FROM_EMAIL=Bad Ass AI <hello@badassai.ca>
CONTACT_RECIPIENT=frank@badassai.ca
ENV
    chmod 600 "$ENV_FILE"
fi

echo "==> Migrate + static"
set -a; . "$ENV_FILE"; set +a
cd "$APP_DIR"
venv/bin/python manage.py migrate --noinput
venv/bin/python manage.py collectstatic --noinput >/dev/null

echo "==> systemd"
cat > /etc/systemd/system/$SERVICE.service <<UNIT
[Unit]
Description=Bad Ass AI (gunicorn)
After=network.target

[Service]
WorkingDirectory=$APP_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$APP_DIR/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:$PORT config.wsgi
Restart=always

[Install]
WantedBy=multi-user.target
UNIT
systemctl daemon-reload
systemctl enable --now $SERVICE
systemctl restart $SERVICE

echo "==> nginx"
cat > /etc/nginx/sites-available/badassai <<NGINX
server {
    listen 80;
    listen [::]:80;
    server_name badassai.ca www.badassai.ca;
    client_max_body_size 10m;
    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
NGINX
ln -sf /etc/nginx/sites-available/badassai /etc/nginx/sites-enabled/badassai
nginx -t && systemctl reload nginx

# Real photo, if the frankalfano project lives on this box
if [ ! -s "$APP_DIR/static/images/.photo-replaced" ]; then
    for CANDIDATE in /srv/frankalfano/static/images/frank-profile.jpg \
                     /home/*/frankalfano/static/images/frank-profile.jpg; do
        if [ -f "$CANDIDATE" ]; then
            cp "$CANDIDATE" "$APP_DIR/static/images/frank-profile.jpg"
            venv/bin/python manage.py collectstatic --noinput >/dev/null
            touch "$APP_DIR/static/images/.photo-replaced"
            echo "==> Replaced placeholder photo from $CANDIDATE"
            break
        fi
    done
fi

if ! venv/bin/python manage.py shell -c \
    "from django.contrib.auth.models import User; import sys; sys.exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" \
    2>/dev/null; then
    echo "==> Create your admin login:"
    venv/bin/python manage.py createsuperuser
fi

echo
echo "Deployed. Checks:"
echo "  curl -sI http://127.0.0.1:$PORT/ | head -1"
echo "  https://badassai.ca  (via Cloudflare)"
echo "  https://badassai.ca/admin/  (leads + services)"
