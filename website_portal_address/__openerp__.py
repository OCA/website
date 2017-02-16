# -*- coding: utf-8 -*-
# Copyright 2016-Today Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Contact's Address Manager In Website Portal",
    "summary": "Contact's Address Manager In Website Portal",
    "version": "9.0.1.0.0",
    "category": "Portal",
    "author": """Serpent Consulting Services Pvt. Ltd.,
                Agile Business Group,
                Odoo Community Association (OCA)""",
    "website": "http://www.serpentcs.com",
    "license": "AGPL-3",
    "depends": [
        "website_portal_contact",
    ],
    "data": [
        "security/ir.rule.csv",
        "views/assets.xml",
        "views/contact_address.xml",
        "views/layout.xml",
    ],
    "installable": True,
}
