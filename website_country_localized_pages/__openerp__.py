# -*- coding: utf-8 -*-
##############################################################################
#
#    © 2015 Agile Business Group (<http://www.agilebg.com>)
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
    'name': 'Country specific pages',
    'summary': "Show website pages localized according to country's visitor",
    'version': '1.0',
    'category': 'Website',
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'ir_ui_view_view.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['ipwhois']
        }
}
