# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Contact Manager In Website Portal",
    "summary": "Allows logged in portal users to manage their contacts",
    "version": "12.0.1.0.0",
    "category": "Portal",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "portal",
        "product",
        "website"
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir.rule.csv",
        "views/assets.xml",
        "views/contact_form.xml",
        "views/contact_tree.xml",
        "views/layout.xml",
    ],
}
