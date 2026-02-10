# Copyright 2026 - Binhex, Adasat Torres de León
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Cloudflare Turnstile on Login",
    "summary": "Add Cloudflare Turnstile captcha to login form",
    "version": "18.0.1.0.0",
    "author": "Binhex, Odoo Community Association (OCA)",
    "maintainers": ["adasatorres"],
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "category": "Website",
    "depends": ["website_cf_turnstile"],
    "assets": {
        "web.assets_frontend": ["website_cf_turnstile_login/static/src/js/*.*"],
    },
}
