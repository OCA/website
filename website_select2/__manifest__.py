# Copyright 2025 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0)

{
    "name": "Feature-rich select boxes",
    "summary": "Integrate select2 in Odoo websites",
    "version": "18.0.1.0.0",
    "development_status": "Beta",
    "category": "Website/Website",
    "website": "https://github.com/OCA/website",
    "author": "Hunki Enterprises BV, Odoo Community Association (OCA)",
    "maintainers": ["hbrunn"],
    "license": "LGPL-3",
    "depends": [
        "web",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_select2/static/lib/select2.js",
            "website_select2/static/lib/select2.css",
            "website_select2/static/lib/select2-bootstrap-5-theme.css",
            "website_select2/static/src/scss/select2-bootstrap-5-theme-overrides.scss",
            "website_select2/static/src/js/website_select2.esm.js",
        ],
    },
}
