# -*- coding: utf-8 -*-

{
    'name': 'Website Portal for Sales',
    'category': 'Website',
    'summary': (
        'Add your sales document in the frontend portal (sales order'
        ', quotations, invoices)'
    ),
    'version': '8.0.1.0.0',
    'author': 'Odoo SA, '
              'MONK Software, '
              'Antiun Ingenieria S.L., '
              'Odoo Community Association (OCA) ',
    'website': 'https://www.odoo.com/, '
               'http://www.wearemonk.com, '
               'http://www.antiun.com',
    'depends': [
        'sale',
        'portal',
        'website_portal',
    ],
    'data': [
        'templates/website_portal_sale.xml',
        'templates/website_portal.xml',
        'templates/website.xml',
        'security/ir.model.access.csv'
    ],
    'demo': [
        'demo/sale_order.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}
