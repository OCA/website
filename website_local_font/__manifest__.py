# Copyright 2023 Onestein- Anjeel Haria
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Website Local Font",
    "summary": "Allows to add local fonts on Odoo website",
    "version": "17.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "installable": True,
    "depends": ["website"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "assets": {
        "website.assets_wysiwyg": [
            "website_local_font/static/src/js/snippets.options.esm.js",
        ],
        "website.assets_editor": [
            "website_local_font/static/src/xml/website.editor.xml",
        ],
        "web._assets_primary_variables": [
            (
                "prepend",
                "website_local_font/static/src/scss/primary_variables.scss",
            ),
        ],
        "web._assets_secondary_variables": [
            (
                "replace",
                "website/static/src/scss/secondary_variables.scss",
                "website_local_font/static/src/scss/secondary_variables.scss",
            ),
        ],
    },
}
