# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'One Step Checkout',
    'category': 'Website',
    'summary': 'Provide an All-In-One Checkout for Your Odoo Customer',
    'version': '1.0',
    'description': """
odoo One Step Checkout
======================
One Step Checkout combines all Odoo Checkout steps into one and removes all unnecessary fields and
questions. Never before has check- out been easier and faster!

Improving the checkout process results in more customers completing their sales, and this has an immediate impact on your bottom line. It is the single most effective technical change you can make to reduce shopping cart abandonment.

Regards Bloopark
    """,
    'author': "bloopark systems GmbH & Co. KG",
    'website': "http://www.bloopark.de",
    'depends': [
        'website_sale_delivery'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_sale_ocs.xml',
        'views/res_config.xml',
        'views/website_sale_osc.xml',
    ],
    'test': [],
    'demo': [],
    'qweb': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
