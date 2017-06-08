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
    "version": "1.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Allows the user to choose if a blogpost header"
               "should have a full screen banner, "
               "a traditional banner or no background at all",
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
    "external_dependencies": {
        'python': [],
    },
}
