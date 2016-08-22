# -*- coding: utf-8 -*-
##############################################################################
#
# Authors: Odoo S.A., Nicolas Petit (Clouder)
# Copyright 2016, TODAY Odoo S.A. Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Website Versioning',
    'category': 'Website',
    'summary': 'Allow to save all the versions of your website and allow to perform AB testing.',
    'version': '9.0.1.0.0',
    'description': """
OpenERP Website CMS
===================

        """,
    'depends': ['website', 'marketing', 'google_account', 'mail'],
    'author': 'Odoo S.A., Nicolas Petit (Clouder)',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/website_version_templates.xml',
        'views/marketing_view.xml',
        'views/website_version_views.xml',
        'views/res_config.xml',
        'data/data.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': False,
}