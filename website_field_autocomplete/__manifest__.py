# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Field - AutoComplete",
    "summary": "Provides an autocomplete field for Website on any model",
    "version": "19.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_field_autocomplete/static/src/js/field_autocomplete.esm.js",
        ],
    },
}
