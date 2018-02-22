# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': "Product Manager in Website Portal for Purchases",
    'category': 'Website',
    'version': '9.0.1.0.0',
    'depends': [
        "stock",
        "website_form",
        'website_sale',
        'website_portal_purchase',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/ir.rule.csv',
        'views/assets.xml',
        'views/layout.xml',
        'views/product_form.xml',
        'views/product_tree.xml',
        'views/website_sale.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'author': 'Antiun Ingeniería S.L., '
              'Incaser Informatica S.L., '
              'Tecnativa, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.tecnativa.com',
    'license': 'LGPL-3',
    'installable': True,
}
