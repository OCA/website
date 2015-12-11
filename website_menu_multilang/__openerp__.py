##############################################################################
#
# OpenERP, Open Source Management Solution
# Copyright (C) 2014 by UAB Versada (Ltd.) <http://www.versada.lt>
# and contributors. See AUTHORS for more details.
#
# All Rights Reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Website Menu Multilanguage',
    'version': '8.0.0.1.0',
    'author': 'Versada UAB,Odoo Community Association (OCA)',
    'category': 'Website',
    'website': 'http://www.versada.lt',
    'description': """
Enables specifying languages for Website Menus.

When website is viewed in specific language only Menus in that language will
be displayed.

TODO:
* Restrict direct URL access for pages of unspecified language
* Proper sitemap.xml generation
* Theme compatibility
* Tests
    """,
    'depends': [
        'website',
    ],
    'data': [
        'view/website.xml',
    ],
    'installable': True,
    'application': False,
}
