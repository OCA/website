# -*- coding: utf-8 -*-
# #############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2014-TODAY Odoo SA (<https://www.odoo.com>).
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
    'name': 'Slides',
    'version': '1.0',
    'summary': 'Share and Publish Videos, Presentations and Documents',
    'category': 'website',
    'author': "Odoo SA, "
              "Incaser Informatica - Sergio Teruel, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/website',
    'depends': ['website', 'website_mail'],
    'data': [
        'view/res_config.xml',
        'view/website_slides.xml',
        'view/website_slides_embed.xml',
        'view/website_slides_backend.xml',
        'view/website_templates.xml',
        'data/website_slides_data.xml',
        'security/ir.model.access.csv',
        'security/website_slides_security.xml'
    ],
    'demo': [
        'data/website_slides_demo.xml'
    ],
    'installable': True,
}
