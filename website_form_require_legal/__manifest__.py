# Copyright 2023 Tecnativa - Carlos Roca
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website Form Require Legal",
    "summary": "Add possibility to require confirm legal terms.",
    "version": "15.0.1.1.0",
    "category": "Website",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": ["views/snippets.xml"],
    "assets": {
        "website.assets_wysiwyg": [
            "website_form_require_legal/static/src/js/options.js"
        ],
        "web.assets_frontend": [
            "website_form_require_legal/static/src/scss/website_form_legal.scss"
        ],
    },
}
