# -*- coding: utf-8 -*-
# Copyright 2018 Lorenzo Battistini
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "Website Legal Page - Shop Integration",
    "summary": "Make legal pages work correctly with website_sale",
    "version": "11.0.1.0.0",
    # see https://odoo-community.org/page/development-status
    "development_status": "Beta",
    "category": "Hidden",
    "website": "https://github.com/OCA/website",
    "author": "Agile Business Group, Odoo Community Association (OCA)",
    # see https://odoo-community.org/page/maintainer-role for a description of the maintainer role and responsibilities
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "website_legal_page",
        "website_sale",
    ],
    "data": [
    ],
}
