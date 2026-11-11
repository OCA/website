# Copyright 2026 ForgeFlow S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website Form Multi Column",
    "summary": "Lay out website form fields across configurable columns"
    " with drag-and-drop.",
    "version": "19.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/website",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "application": False,
    "installable": True,
    "depends": ["html_editor", "website"],
    "assets": {
        "web.assets_frontend": [
            "website_form_multi_column/static/src/scss/form_columns.scss",
        ],
        "website.website_builder_assets": [
            "website_form_multi_column/static/src/builder/**/*",
        ],
    },
}
