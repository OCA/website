# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Invoices Separated By Type In Website Portal",
    "summary": "Display in and out invoices in separate controllers",
    "version": "9.0.1.0.0",
    "category": "Website",
    "website": "https://tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_portal_sale_v10",
        "website_portal_purchase",
    ],
    "data": [
        "views/layout.xml",
        "views/invoices.xml",
    ],
}
