# -*- coding: utf-8 -*-
# © 2016 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Remove odoo.com bindings on website",
    "version": "9.0.1.0.0",
    "author": "Tecnativa,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'website': 'http://www.tecnativa.com',
    "category": "Website",
    "depends": [
        'website',
    ],
    "data": [
        "views/disable_odoo.xml",
    ],
    "installable": True,
}
