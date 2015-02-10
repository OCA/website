# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
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
    'name': 'Link event to tasks',
    'version': '1.0',
    'category': 'Marketing',
    'author': 'Serv. Tecnolog. Avanzados - Pedro M. Baeza, '
              'Antiun Ingeniería S.L.',
    'website': 'http://www.serviciosbaeza.com, http://www.antiun.com',
    'depends': [
        'event',
        'project',
    ],
    'data': [
        'views/event_event_view.xml',
        'views/project_task_view.xml',
    ],
    "installable": True,
}
