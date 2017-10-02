# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Layout Options and Extensions for Blog",
    "version": "8.0.1.0.0",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Adds options and layout for the blog",
    "depends": [
        'website_blog'
    ],
    "data": [
        'views/templates.xml',
        'views/views.xml',
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
