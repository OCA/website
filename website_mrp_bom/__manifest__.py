# Copyright 2018-2021 ForgeFlow, S.L. (https://www.forgeflow.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website MRP BOM",
    "category": "Website",
    "summary": "Bill of Materials Module for Website",
    "version": "14.0.1.0.0",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/website",
    "depends": ["mrp", "website", "website_product"],
    "data": [
        "security/ir.model.access.csv",
        "security/website_mrp_bom.xml",
        "views/website_mrp_bom_templates.xml",
        "views/mrp_bom_views.xml",
    ],
    "installable": True,
    "auto_install": False,
}
