# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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
    # Theme information
    'name': "Event register allow duplicates",
    'description': """
Event register allow duplicates
===============================

This module include new button to allow register duplicate.
    """,
    'category': 'Event',
    'version': '1.0',
    'depends': [
        'website_event_register_free_with_sale',
    ],
    'external_dependencies': {},
    'data': ['views/event_event_view.xml'],
    'qweb': [],
    'author': 'Antiun Ingenieria S.L.',
    'maintainer': 'Antiun Ingenieria S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
