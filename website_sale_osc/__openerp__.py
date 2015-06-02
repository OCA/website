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
    'summary': 'Provide an All-In-One Checkout for your website e-commerce',
    'version': '1.0',
    'author': "bloopark systems GmbH & Co. KG ,"
              "Odoo Community Association (OCA)",
    'website': "http://www.bloopark.de",
    'depends': [
        'website_sale_delivery',
        'website'
    ],
    'data': [
        'security/website_sale_ocs.xml',
        'views/res_config.xml',
        'views/website_sale_osc.xml',
    ],
    'installable': True,
    'auto_install': False,
}
