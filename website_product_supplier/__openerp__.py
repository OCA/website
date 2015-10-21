# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': "Website Product Supplier",
    'category': 'Website',
    'version': '8.0.1.0.0',
    'depends': [
        'auth_supplier',
        'website_portal',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/website_product_supplier.xml',
        'views/product_supplier_view.xml',
        'security/website_product_supplier_security.xml',
    ],
    'author': 'Incaser Informatica S.L., '
              'Antiun Ingeniería S.L., '
              'Odoo Community Association (OCA)',
    'website': 'http://www.incaser.es',
    'license': 'AGPL-3',
    'installable': True,
}
