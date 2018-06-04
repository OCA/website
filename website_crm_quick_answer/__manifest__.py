# -*- coding: utf-8 -*-
# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Quick answer for website contact form",
    "summary": "Add an automatic answer for contacts asking for info",
    'category': 'Customer Relationship Management',
    'version': '11.0.1.0.0',
    'depends': [
        'base_automation', 'website_crm',
    ],
    'data': [
        "data/automation.xml",
    ],
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'license': 'AGPL-3',
    'installable': True,
}
