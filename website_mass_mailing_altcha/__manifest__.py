# Copyright 2026 Nitrokey GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Privacy Friendly Captcha - Newsletter",
    "summary": "Support newsletter subscription with ALTCHA",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Nitrokey GmbH,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website_altcha",
        "website_mass_mailing",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_mass_mailing_altcha/static/src/*.esm.js",
        ],
        "web.assets_tests": [
            "website_mass_mailing_altcha/static/tests/tours/*.esm.js",
        ],
    },
    "demo": [
        "demo/newsletter_page.xml",
    ],
    "auto_install": True,
}
