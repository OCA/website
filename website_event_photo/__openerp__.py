# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
#                 Javier Iniesta <javieria@antiun.com>
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
##############################################################################

{
    'name': "Website Event Photo",
    'category': 'Tools',
    'version': '1.0',
    'depends': [
        'website_event'
    ],
    'data': [
        'views/event_event.xml'
    ],
    'author': 'Antiun Ingeniería S.L.',
    'maintainer': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
