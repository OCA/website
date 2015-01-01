# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2010-2014 Elico Corp. All Rights Reserved.
#    Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
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
{'name': 'Website reCAPTCHA',
 'version': '1.0',
 'category': 'Website',
 'depends': ['website'],
 'author': 'Elico Corp',
 'license': 'AGPL-3',
 'website': 'https://www.elico-corp.com',
 'description': """
OpenERP reCAPTCHA
=================
This modules allows you to integrate Google reCAPTCHA to your website forms.
You can configure your Google reCAPTCHA private and public keys
in "Settings" -> "Website Settings"

You will need to install the "Website CRM reCAPTCHA module"
to use it in your "contact us" page
""",
 'data': [
     'views/website_templates.xml',
     'views/website_view.xml',
     'views/res_config.xml',
 ],
 'installable': True,
 'auto_install': False}
