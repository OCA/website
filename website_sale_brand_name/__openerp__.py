#-*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2015-Today BrowseInfo (<http://www.browseinfo.in>)
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
    'name': 'Website Sale Product Brand Name',
    'category': 'Website',
    'summary': 'Put Brand Name On Product',
    'website': 'http://www.browseinfo.in',
    'version': '1.0',
    'description': """
Create Brand Name in Product Variants.
======================================

        """,
    'author': 'BrowseInfo',
    'website': 'http://www.browseinfo.in',
    'depends': ['base', 'website', 'sale',
                'website_sale', 'product_brand_name'],
    'data': [
        'views/templates.xml',
        'views/payment.xml',
        'views/sale_order.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
