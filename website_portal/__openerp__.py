# -*- coding: utf-8 -*-
{
    'name': 'Website Portal',
    'category': 'Website',
    'summary': 'Account Management Frontend for your Customers',
    'version': '1.0',
    'license': 'LGPL-3',
    'author': 'Odoo SA, MONK Software',
    'website': (
        'https://www.odoo.com/, http://www.wearemonk.com, '
        'https://github.com/OCA/website'
    ),
    'depends': [
        'website',
    ],
    'data': [
        'templates/website.xml',
        'templates/website_portal.xml',
    ],
    'installable': True,
}
