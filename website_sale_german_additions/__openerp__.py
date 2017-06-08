# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2010-2013 OpenERP s.a. (<http://openerp.com>).
#    Copyright (C) 2014 copado MEDIA UG (<http://www.copado.de>).
#    Author Mathias Neef <mn[at]copado.de>
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
    'name': 'eCommerce German additions',
    'category': 'Website',
    'summary': 'German additions for eCommerce (B2C)',
    'version': '0.1',
    'description': """
German additions for eCommerce (B2C)
==========================

This addon installed necessary additions in accordance with statutory requirements in Germany.

Overview
--------
 - adds terms page
 - adds revocation page
 - adds delivery page
 - adds privacy page
 - adds imprint page
 - adds an easy built-in address snippet to content blocks
 - adds "incl. VAT, plus shipping costs" to every price
 - adds terms and revocation popup on payment site; both are taken from terms and revocation page on the frontend
 
Todo
----
 - add VAT-percentage to every "incl. VAT"
 - translate all into german
 - create a email template which inherits all statutory required informations
 - ...

Contact for questions
---------------------
copado MEDIA UG - Unterdorfstr. 29 - 77948 Friesenheim - Germany - Phone: +49 7821 32725 20 - info@copado.de - http:www.copado.de
        """,
    'author': 'copado MEDIA UG, Mathias Neef',
    'depends': ['website_sale'],
    'data': [
        'views/wsga_views.xml',
        'views/wsga_templates.xml',
        'views/wsga_snippets.xml',
        'data/data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
}