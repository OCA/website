# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Product Packaging Price Manager in Website Portal for Purchases",
    "summary": "Product packaging prices management for your suppliers",
    "version": "9.0.1.0.0",
    "category": "Website",
    "website": "https://www.tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "sale_packaging_price",
        "website_portal_purchase_product",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/ir.rule.csv",
        "views/assets.xml",
        "views/product_form.xml",
    ],
    "qweb": [
        "static/src/xml/packaging.xml",
    ],
}
