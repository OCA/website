# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV <http://therp.nl>.
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
    "name": "Optional Background image for Blog Posts",
    "summary": "Choose how to display Blog Post headers",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://odoo-community.org/",
    "author": "Therp BV,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        'website_blog'
    ],
    "data": [
        "views/views.xml",
        "views/templates.xml",
    ],
    "css": [
        "static/src/css/website_blog_nobkimage.css",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
