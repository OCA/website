# -*- coding: utf-8 -*-
##############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C)2004-TODAY Tech Receptives(<https://www.techreceptives.com>)
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
{'name': 'Website reCAPTCHA Reloaded',
 'version': '1.0',
 'category': 'Website',
 'depends': ['website'],
 'author': 'Tech Receptives',
 'license': 'AGPL-3',
 'website': 'https://www.techreceptives.com',
 'description': """
Odoo Website reCAPTCHA Reloaded
================================
This modules allows you to integrate Google reCAPTCHA v2.0 to your website forms.
You can configure your Google reCAPTCHA site and public keys
in "Settings" -> "Website Settings"

You will need to install various website_<module>_recaptcha modules 
to use it in your various pages.
""",
 'data': [
          'views/website_view.xml',
          'views/res_config.xml',
 ],
 'installable': True,
 'auto_install': False
}
