# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Social Media Icon Extension",
    'summary': """Extension for the social media icons from the odoo core""",
    'author': "bloopark systems GmbH & Co. KG, "
              "Odoo Community Association (OCA)",
    'website': "http://www.bloopark.de",
    'license': 'AGPL-3',
    'category': 'Social Media',
    'version': '1.0',

    'depends': [
        'base',
        'website',
        'website_blog'
    ],

    'data': [
        'views/website_templates.xml',
        'views/website_views.xml',
        'views/website_blog_template.xml',
        'views/res_config.xml',
    ],
}
