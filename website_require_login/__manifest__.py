# Copyright 2020 Advitus MB
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Website Login Required",
    "category": "Website",
    "version": "15.0.1.0.0",
    "author": "Advitus MB, Ooops, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "LGPL-3",
    "depends": [
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/website_auth_url.xml",
        "data/ir_actions.xml",
        "data/ir_ui_menu.xml",
    ],
    "installable": True,
}
