# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Quick answer for website contact form",
    "summary": "Add an automatic answer for contacts asking for info",
    'category': 'Customer Relationship Management',
    'version': '9.0.1.0.0',
    'depends': [
        'base_action_rule',
        'website_crm',
    ],
    'data': [
        "data/automation.xml",
    ],
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'license': 'AGPL-3',
    'installable': True,
}
