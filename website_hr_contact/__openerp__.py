# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of website_hr_contact,
#     an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     website_hr_contact is free software:
#     you can redistribute it and/or modify it under the terms of the GNU
#     Affero General Public License as published by the Free Software
#     Foundation,either version 3 of the License, or (at your option) any
#     later version.
#
#     website_hr_contact is distributed
#     in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
#     even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#     PURPOSE.  See the GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with website_hr_contact.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "hR Address Book",

    'summary': """
        Display your hr address book in your website""",

    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': "http://acsone.eu",
    'category': 'Website',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'website_hr',
    ],

    'data': [
        'views/website_hr_contact_templates.xml',
        'data/website_hr_contact_data.xml',
    ],
}
