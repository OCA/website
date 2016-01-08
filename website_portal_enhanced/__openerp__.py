# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Today Serpent Consulting Services PVT. LTD.
#     (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

{
    'name': 'Website Portal Enhanced',
    'category': 'Website',
    'summary': """Edit and view users personal information and change
                users profile photo.""",
    'version': '8.0.1.0.0',
    "author": """Serpent Consulting Services Pvt. Ltd.,
                 Odoo Community Association (OCA)""",
    'depends': [
        'website_portal',
    ],
    'data': [
        'views/website_profile.xml',
        'views/assets.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
