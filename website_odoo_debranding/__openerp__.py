# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa, S.L. - Vicent Cubells
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Remove odoo.com bindings on website",
    "version": "10.0.1.0.0",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "website": "http://www.tecnativa.com",
    "license": "LGPL-3",
    "category": "Website",
    "depends": [
        'website',
    ],
    "data": [
        "views/disable_odoo.xml",
    ],
    "installable": True,
}
