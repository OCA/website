# Copyright 2017 Tecnativa - Jairo Llopis
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Website Form Builder",
    "summary": "Build customized forms in your website",
    "version": "11.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_form",
    ],
    "data": [
        "templates/assets.xml",
        "templates/snippets.xml",
        "views/ir_model.xml",
    ],
    "demo": [
        "demo/assets.xml",
        "demo/ir_model.xml",
    ],
}
