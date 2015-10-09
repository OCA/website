# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Endika Iglesias <endikaig@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Add Facebook comments on blog posts",
    'category': 'Website',
    'version': '8.0.1.0.0',
    'depends': [
        'base',
        'website',
        'website_blog',
    ],
    'data': [
        'views/blog_post_complete_view.xml',
        'views/facebook_settings_view.xml',
    ],
    "author": "Antiun Ingeniería S.L., "
              "Odoo Community Association (OCA)",
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
}
