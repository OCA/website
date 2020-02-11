# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": 'Website page security',
    "version": "10.0.7.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "website",
    "summary": 'Add group security to pages',
    "depends": [
        'website',
        'base_suspend_security',
    ],
    "data": [
        'views/assets.xml',
        'views/forbidden_page.xml',
        'views/ir_ui_view.xml',
        'views/templates.xml',
        'security/ir_rules.xml',
    ],
    'post_init_hook': 'post_init',
    "application": False,
    "installable": True,
}
