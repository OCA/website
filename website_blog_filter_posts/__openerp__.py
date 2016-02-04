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
    'name': 'Filter Blog Posts',
    'summary': 'Add some filters in blog.',
    'category': 'Website',
    "license": "AGPL-3",
    'author': "bloopark systems GmbH & Co. KG, Odoo Community Association (OCA)",
    'website': "http://www.bloopark.de",

    'version': '9.0.1.0.0',

    'data': [
        'views/assets.xml',
        'views/templates.xml'
    ],
    'depends': [
        'website_blog',
    ],
}
