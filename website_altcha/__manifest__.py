# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Friendly Captcha",
    "summary": """Use Friendly Captcha for verifying users""",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Dixmit,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_altcha/static/src/**/*.esm.js",
            "website_altcha/static/src/**/*.xml",
            "website_altcha/static/src/**/*.scss",
        ],
        "web.altcha_libs": [
            "website_altcha/static/lib/altcha.js",
            "website_altcha/static/lib/altcha-l10n.js",
        ],
    },
    "post_init_hook": "post_init_hook",
    "data": [],
    "demo": [],
}
