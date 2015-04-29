# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
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
    "name": "Website Sale Customer",
    "version": "1.0",
    "author": "Abstract.it",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Customer views for ecommerce",
    "depends": [
        'web',
        'website_sale',
        'base_action_rule',
    ],
    "data": [
        'data/website.xml',
        'data/emails.xml',
        'data/action_rules.xml',
        'view/templates_account.xml',
        'view/templates_orders.xml',
    ],
    "demo": [
    ],
    "test": [
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
