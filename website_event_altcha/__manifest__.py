# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Privacy Friendly Captcha - Event Registration",
    "summary": "Support event registration with ALTCHA",
    "version": "18.0.1.0.0",
    "license": "AGPL-3",
    "author": "Hunki Enterprises BV,Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "website": "https://github.com/OCA/website",
    "depends": [
        "website_altcha",
        "website_event",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_event_altcha/static/src/*.esm.js",
        ],
        "web.assets_tests": [
            "website_event_altcha/static/tests/tours/website_event_altcha.esm.js",
        ],
    },
    "auto_install": True,
}
