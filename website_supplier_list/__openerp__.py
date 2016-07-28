# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Supplier List',
    'version': '8.0.1.0.0',
    'summary': 'Publish Your Suppliers References',
    'author': 'OpenSynergy Indonesia,Odoo Community Association (OCA)',
    'website': 'https://github.com/mikevhe18',
    'category': 'Website',
    'depends': [
        'crm_partner_assign',
        'purchase',
        'website_partner'
        ],
    'data': [
        'security/website_supplier_list.xml',
        'views/assets.xml',
        'views/website_supplier.xml',
        'views/res_partner_view.xml'
    ],
    'installable': True,
}
