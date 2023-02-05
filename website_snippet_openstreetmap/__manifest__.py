# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Snippet OpenStreetMap",
    "category": "Website",
    "version": "15.0.1.0.0",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "depends": [
        "base_geolocalize",
        "website",
    ],
    "data": [
        "views/snippets/s_openstreetmap.xml",
        "views/snippets/snippets.xml",
    ],
    "demo": [
        "demo/res_partner_demo.xml",
    ],
    "assets": {
        "website.assets_wysiwyg": [
            ("include", "web._assets_helpers"),
            "website_snippet_openstreetmap/static/src/snippets/s_openstreetmap/options.js",
        ],
        "web.assets_frontend": [
            "website_snippet_openstreetmap/static/src/js/utils.js",
        ],
    },
}
