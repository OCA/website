# -*- coding: utf-8 -*-
# Copyright 2018 Jarsa Sistemas <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Hotjar analytics",
    "version": "10.0.1.0.0",
    "author": "Jarsa Sistemas,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Track website users using Hotjar",
    "depends": [
        "website",
    ],
    "data": [
        "views/website_config_settings.xml",
        "views/website.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
