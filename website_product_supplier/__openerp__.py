# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': "Website Product Supplier",
    'category': 'Website',
    'version': '8.0.1.0.0',
    'depends': [
        'website_sale',
        'website_portal_purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_supplier_view.xml',
        'views/website_portal.xml',
        'views/assets.xml',
        'security/website_product_supplier_security.xml',
    ],
    'images': [],
    'qweb': ['static/src/xml/*.xml'],
    'author': 'Antiun Ingeniería S.L., '
              'Incaser Informatica S.L., '
              'Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
