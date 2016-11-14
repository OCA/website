# -*- coding: utf-8 -*-
# © 2016 Tecnativa, S.L. - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Remove odoo.com bindings on website",
    "version": "9.0.1.0.0",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.tecnativa.com",
    "license": "AGPL-3",
    "category": "Website",
    "depends": [
        'website',
    ],
    "data": [
        "views/disable_odoo.xml",
    ],
    "installable": True,
}
