# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria S.L. (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
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
    "name": "Event register free form fields",
    "version": "1.0",
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    "category": "Event Management",
    "description": """
Event register free form fields
===============================

This module edit the event form and add or
remove fields (phone, zip, promo source)
and you check required or not
    """,
    "depends": ['base', 'event', 'website_event_register_free_with_sale',
                'website_sale'],
    "data": [
        'data/default_data.xml',
        'views/event_registration.xml',
        'views/event_event_view.xml',
        'views/event_registration_fields_view.xml',
        'views/event_registration_field_view.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
