# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

{
    'name': 'Website Portal for Purchases',
    'category': 'Website',
    'summary': "Add purchase orders and quotation in the frontend portal",
    'version': '10.0.1.1.0',
    'depends': [
        'auth_supplier',
        'purchase',
        'website_portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/portal_security.xml',
        'views/assets.xml',
        'views/layout.xml',
        'views/quotes.xml',
        'views/orders.xml',
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Incaser Informatica S.L., '
              "Tecnativa, "
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'license': 'LGPL-3',
    'installable': True,
}
