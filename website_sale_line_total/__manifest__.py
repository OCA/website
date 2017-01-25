# -*- coding: utf-8 -*-
# Copyright 2017 Specialty Medical Drugstore, LLC
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Line Total",
    "summary": "Adds separate columns for unit price and total price",
    "version": "10.0.1.0.0",
    "category": "E-commerce",
    "website": "https://www.github.com/OCA/website",
    "author": "SMDrugstore, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
        "website_sale",
    ],
    "data": [
        "views/website_sale_line_total_view.xml",
    ],
}
