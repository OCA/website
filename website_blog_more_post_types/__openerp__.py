# -*- coding: utf-8 -*-
# (C) 2015 Therp BV <http://therp.nl>.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Blog post visualization options',
    'version': '8.0.1.0.0',
    'author': 'Therp BV,'
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'category': 'Website',
    'website': 'https://odoo-community.org/',
    'depends': [
        'website_blog'
    ],
    'data': [
        'views/teaser.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': False,
}
