# Copyright 2018-2021 ForgeFlow S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Website Product",
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "category": "Website",
    "summary": "Product Module for Website",
    "author": "ForgeFlow, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": ["product", "website", "stock"],
    "data": [
        "views/website_product_templates.xml",
        "views/product_views.xml",
        "security/website_product.xml",
        "security/ir.model.access.csv",
    ],
    "qweb": ["static/src/xml/website.product.backend.xml"],
    "installable": True,
    "auto_install": False,
}
