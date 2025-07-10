# Copyright 2023 Studio73 - Miguel Gandia <miguel@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Google Analytics 4",
    "summary": "Google Analytics 4 integration",
    "category": "Website",
    "version": "16.0.1.0.0",
    "author": "Studio73, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": ["views/website_templates.xml"],
    "assets": {
        "web.assets_frontend": [
            "website_google_analytics_4/static/src/js/website_sale_tracking.js",
        ],
    },
    "installable": True,
}
