# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Hide website",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Hide the website from the frontend",
    "depends": [
        'website',
    ],
    "data": [
        "data/ir_ui_menu.xml",
        'views/templates.xml',
    ],
    "post_init_hook": 'post_init_hook',
}
