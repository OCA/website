# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Add To Chart Button Visibility',
    'version': '8.0.1.0.0',
    'summary': 'Enables to controlling button add to cart per product',
    'author': 'OpenSynergy Indonesia,Odoo Community Association (OCA)',
    'website': 'https://opensynergy-indonesia.com',
    'category': 'Website',
    'depends': ['website_sale'],
    'data': [
        'views/product_view.xml',
        'views/website_sale_template.xml'
    ],
    'installable': True,
    'license': 'AGPL-3',
}
