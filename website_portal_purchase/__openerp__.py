# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Website Portal for Purchases',
    'category': 'Website',
    'summary': (
        'Add your purchase document in the frontend portal (purchase order'
        ', request for quotations, supplier invoices)'
    ),
    'version': '8.0.1.0.0',
    'depends': [
        'auth_supplier',
        'purchase',
        'website_portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_portal_purchase_security.xml',
        'views/website_portal_purchase.xml',
        'views/website_portal.xml',
        'views/website.xml',
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Incaser Informatica S.L., '
              'Odoo Community Association (OCA)',
    'website': 'http://www.incaser.es',
    'license': 'AGPL-3',
    'installable': True,
}
