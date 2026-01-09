##############################################################################
#
#    Kardec
#    Copyright (C) 2016-Today Kardec (<http://www.kardec.net>).
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
    "name": "Website - no index, no follow",
    "version": "14.0.1.0.0",
    "category": "Website",
    "summary": "Deactivate option for website indexing by search engines",
    "license": "AGPL-3",
    "author": "Kardec, Therp B.V., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": ["website"],
    "data": [
        "views/res_config_settings.xml",
        "views/assets.xml",
        "views/website_layout.xml",
        "views/website_navbar.xml",
    ],
    "assets": {
        "website.assets_editor": [
            "website_noindex/static/src/css/styles.css",
            "website_noindex/static/src/js/website_editor.js",
        ],
    },
    "installable": True,
    "application": False,
}
