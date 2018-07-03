# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Backend views for website",
    "version": "9.0.1.0.0",
    "author": "Therp BV, LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Dependency",
    "summary": "Hook backend views into your website frontend",
    "depends": [
        'web',
        'website',
    ],
    "data": [
        'view/templates.xml',
    ],
    "demo": [
        "view/demo.xml",
    ],
    'installable': True,
}
