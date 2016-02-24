# -*- encoding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Daniel Góme-Zurita <danielgz@antiun.com>
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
    # Theme information
    'name': "Antiun Backend Theme",
    'category': 'Theme',
    'version': '1.0',

    # Dependencies
    'depends': [
        'web',
    ],
    'external_dependencies': {},

    # Views templates, pages, menus, options and snippets
    'data': [
        'views/backend.xml',
        # 'reports/common.xml',
    ],

    # Qweb templates
    'qweb': [
        'static/src/xml/backend.xml',
    ],

    # Your information
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',

    # Technical options
    'demo': [],
    'test': [],
    'installable': True,
    # 'auto_install':False,
    # 'active':True,

}
