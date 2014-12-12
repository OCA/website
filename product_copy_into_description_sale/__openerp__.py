# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

{
    'name': 'Product Copy Into Description Sale',
    'version': '1.1',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'category': 'Sales',
    'summary': 'Copy a set of value of fields and their titles into the description_sale',
    'description': """
Sale Copy Into Description Sale
===============================
In Sales Module, this module allows to copy fields and their title of
the product.template into the description_sale.

The description_sale is fed by the translated name of the field to help the
reading


Contributors
------------
* Jordi Riera (jordi.riera@savoirfairelinux.com)
* William BEVERLLY (william.beverlly@savoirfairelinux.com)

""",
    'depends': [
        'product',
        'website_sale',
        'product_template_header'
    ],
    'external_dependencies': {},
    'data': [
        'views/product_template.xml'

    ],
    'installable': True,
}
