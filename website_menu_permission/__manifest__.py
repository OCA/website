# Copyright 2017 Simone Orsi.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Menu Permission',
    'version': '11.0.1.0.0',
    'author': 'Camptocamp,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'license': 'LGPL-3',
    'category': 'Website',
    'summary': 'Allow to show/hide website menu items by user groups.',
    'depends': [
        'website',
    ],
    'data': [
        'security/record_rules.xml',
        'views/website_views.xml',
    ],
    'installable': True,
}
