# Copyright 2026 Tecnativa - Pilar Vargas
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Website Mail Cloudflare Turnstile",
    "summary": "Adds Cloudflare Turnstile support to website mail follow actions",
    "version": "18.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": ["website_mail", "website_cf_turnstile"],
    "assets": {
        "web.assets_frontend": [
            "website_mail_turnstile/static/src/js/website_mail_turnstile.esm.js",
        ],
    },
}
