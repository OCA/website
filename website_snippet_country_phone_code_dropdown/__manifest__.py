# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Website Snippet Country Phone Code Dropdown",
    "summary": "Allow to select country in a dropdown, and fill with phone code",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_snippet_country_dropdown"],
    "data": ["views/snippets.xml"],
    "demo": ["demo/pages.xml"],
    "assets": {
        "web.assets_tests": [
            "/website_snippet_country_phone_code_dropdown/static/src/js/"
            "web_tour_country_phone_code_dropdown.js"
        ],
        "web.assets_frontend": [
            "/website_snippet_country_phone_code_dropdown/static/src/css/style.scss",
            "/website_snippet_country_phone_code_dropdown/static/src/js/"
            "website_snippet_country_phone_code_dropdown.js",
        ],
    },
}
