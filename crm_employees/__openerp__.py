# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                       Antonio Espinosa <antonioea@antiun.com>
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
    'name': 'Employees in CRM',
    'version': '1.0',
    'category': 'Customer Relationship Management',
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'depends': [
        'crm',
    ],
    'data': [
        'views/crm_employees_range_view.xml',
        'views/crm_lead_view.xml',
        'views/res_partner_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
