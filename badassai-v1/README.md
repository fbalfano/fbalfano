# badassai.ca — V1

Django site for **Bad Ass AI** (Agency · Coaching · Consulting).
Dark "Ignition" design system: Anton / Archivo / IBM Plex Mono, ember-orange
accent, self-hosted fonts, ambient node-mesh background.

## What's here

- **Pages**: Home, About, Services, Members, Newsletter, Contact
  (navbar + footer in `templates/base.html`).
- **Services are database-driven** — edit them in the admin
  (`/admin/core/service/`); the Services page and home teaser render whatever
  is active, in `order`. Three launch services are seeded by migration.
- **Leads pipeline** — contact-form and members-waitlist submissions create a
  `Lead` (status: new → contacted → qualified → **client** → closed). Manage
  and promote leads at `/admin/core/lead/` (bulk action: "Mark selected leads
  as CLIENT"). Newsletter signups are stored as `NewsletterSubscriber`.
- **Email notifications** — every lead also emails `frank@badassai.ca`, sent
  from `hello@badassai.ca` via Migadu SMTP. A mail failure never loses the
  lead (it's saved first; the error is logged).
- **SEO standard** (repo `django-standard`): `/sitemap.xml` with honest
  `lastmod` (Services page uses the latest DB edit), `/robots.txt`,
  `/llms.txt`, Sites framework seeded with `badassai.ca`.
- **extras/email-signature.html** — Frank's email signature (open in a
  browser, select-all, copy, paste into the mail client's signature box).

## Replace the placeholder photo

`static/images/frank-profile.jpg` is a committed placeholder. Replace it with
the real photo — same file already used by the frankalfano project:

    cp ../frankalfano/static/images/frank-profile.jpg static/images/frank-profile.jpg

Then re-run `collectstatic` on the server.

## Local development

    python3 -m venv venv && venv/bin/pip install -r requirements.txt
    venv/bin/python manage.py migrate
    venv/bin/python manage.py createsuperuser
    DJANGO_DEBUG=1 DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend \
        venv/bin/python manage.py runserver

## Deploy on Hetzner (behind Cloudflare)

1. **Code + venv**

       git clone <repo> /srv/badassai && cd /srv/badassai/badassai-v1
       python3 -m venv venv && venv/bin/pip install -r requirements.txt

2. **Environment** — copy `.env.example` to `/etc/badassai.env`, fill in a real
   `DJANGO_SECRET_KEY` (e.g. `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`)
   and the Migadu password for `hello@badassai.ca`. `chmod 600 /etc/badassai.env`.

3. **Migrate + static + admin user**

       set -a; . /etc/badassai.env; set +a
       venv/bin/python manage.py migrate
       venv/bin/python manage.py collectstatic --noinput
       venv/bin/python manage.py createsuperuser

4. **systemd** — `/etc/systemd/system/badassai.service`:

       [Unit]
       Description=Bad Ass AI (gunicorn)
       After=network.target

       [Service]
       WorkingDirectory=/srv/badassai/badassai-v1
       EnvironmentFile=/etc/badassai.env
       ExecStart=/srv/badassai/badassai-v1/venv/bin/gunicorn \
           --workers 3 --bind 127.0.0.1:8001 config.wsgi
       Restart=always

       [Install]
       WantedBy=multi-user.target

       # systemctl daemon-reload && systemctl enable --now badassai

5. **Reverse proxy** — point the badassai.ca vhost at `127.0.0.1:8001`
   (whitenoise serves static files, so no static/alias config is needed).
   Nginx example:

       server {
           listen 80;
           server_name badassai.ca www.badassai.ca;
           location / {
               proxy_pass http://127.0.0.1:8001;
               proxy_set_header Host $host;
               proxy_set_header X-Forwarded-Proto $scheme;
               proxy_set_header X-Real-IP $remote_addr;
           }
       }

   Cloudflare is already proxying badassai.ca → this box; keep Cloudflare SSL
   mode "Full (strict)" with your existing origin cert setup.

6. **Smoke test** — submit `/contact/`, confirm the email arrives at
   frank@badassai.ca and the lead appears at `/admin/core/lead/`.
