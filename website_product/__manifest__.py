# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Product',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'Product Module for Website',
    'author': 'Eficent, '
              'Odoo Community Association (OCA)',
    'website': "https://github.com/OCA/website",
    'depends': ['product', 'website', 'stock'],
    'data': [
        'views/website_product_templates.xml',
        'views/product_views.xml',
        'security/website_product.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': ['static/src/xml/website.product.backend.xml'],
    'installable': True,
    'auto_install': False,
}
