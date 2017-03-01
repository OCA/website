# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Calendar Snippet',
    'category': 'Website',
    'summary': 'Calendar on website.',
    'version': '9.0.1.0.0',
    'author': 'Onestein,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': [
        'website',
        'calendar',
        'web'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'templates/assets.xml',
        'templates/snippets.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
