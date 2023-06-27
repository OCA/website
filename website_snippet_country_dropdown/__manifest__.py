# Copyright 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Website Snippet Country Code Dropdown",
    "summary": "Allow to select country in a dropdown",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, " "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": ["views/snippets.xml"],
    "demo": ["demo/pages.xml"],
    "assets": {
        "web.assets_tests": [
            "/website_snippet_country_dropdown/static/src/js/"
            "web_tour_country_dropdown.js"
        ],
        "web.assets_frontend": [
            "/website_snippet_country_dropdown/static/src/css/style.scss",
            "/website_snippet_country_dropdown/static/src/js/"
            "website_snippet_country_dropdown.js",
        ],
        "web.assets_qweb": [
            "/website_snippet_country_dropdown/static/src/xml/country_dropdown.xml"
        ],
    },
}
