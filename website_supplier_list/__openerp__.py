# -*- coding: utf-8 -*-
# © 2016 Michael Viriyananda
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Supplier List',
    'version': '8.0.1.0.0',
    'summary': 'Publish Your Suppliers References',
    'author': 'Michael Viriyananda,Odoo Community Association (OCA)',
    'website': 'https://github.com/mikevhe18',
    'category': 'Website',
    'depends': [
        'purchase',
        'website_partner',
        'website_google_map'
        ],
    'data': [
        'views/website_supplier.xml',
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
