# -*- coding: utf-8 -*-
{
    'name': 'Website Portal',
    'category': 'Website',
    'summary': 'Account Management Frontend for your Customers',
    'version': '8.0.1.0.0',
    'license': 'LGPL-3',
    'author': 'Odoo SA, MONK Software, Antiun Ingeniería S.L.',
    'website': (
        'https://www.odoo.com/, http://www.wearemonk.com, '
        'https://github.com/OCA/website'
    ),
    'depends': [
        'auth_signup',
        'website',
    ],
    'data': [
        'templates/website.xml',
        'templates/website_portal.xml',
    ],
    'installable': True,
}
