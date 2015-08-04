# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd.
#                                     (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Product Brand Filtering in Website',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    'website': 'http://www.serpentcs.com',
    'summary': '',
    'version': '1.0',
    'description': """
Product Brand Filtering in Website
==================================
Allows to use product brands as filtering for products in website.
This Module depends on product_brand module :
->https://github.com/OCA/product-attribute/tree/8.0/product_brand
The blog here explains the HOWTO :
http://www.serpentcs.com/serpentcs-odoo-ecommerce-shop-brands-contribution
The Youtube Video is here :
https://www.youtube.com/watch?feature=player_embedded&v=LkV5umivylw

        """,
    'depends': [
        'product_brand',
        'website_sale'
    ],
    'data': [
        "security/ir.model.access.csv",
        "views/product_brand.xml",
    ],
    'installable': True,
    'auto_install': False,
}
