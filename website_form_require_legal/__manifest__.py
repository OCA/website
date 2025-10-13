# Copyright 2023 Tecnativa - Carlos Roca
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website Form Require Legal",
    "summary": "Add possibility to require confirm legal terms.",
    "version": "19.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "application": False,
    "installable": True,
    "depends": ["html_editor", "website"],
    "assets": {
        "web.assets_frontend": [
            "website_form_require_legal/static/src/scss/website_form_legal.scss",
            "website_form_require_legal/static/src/js/terms_and_conditions.esm.js",
            "website_form_require_legal/static/src/js/submit_button.esm.js",
        ],
        "website.website_builder_assets": [
            "website_form_require_legal/static/src/builder/**/*",
        ],
    },
}
