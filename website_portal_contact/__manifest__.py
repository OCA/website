# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Contact Manager In Website Portal",
    "summary": "Allows logged in portal users to manage their contacts",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "category": "Portal",
    "website": "https://tecnativa.com/",
    "version": "14.0.1.0.0",
    "depends": ["portal", "website"],
    "data": [
        "views/assests.xml",
        "security/ir.model.access.csv",
        "security/ir.rule.csv",
        "views/contact_portal_template.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
