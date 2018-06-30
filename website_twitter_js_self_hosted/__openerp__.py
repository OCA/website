# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Multiple Twitter Feeds and user stats with widget support"
            " and no external javascript",
    "version": "8.0.1.0.0",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "depends": [
        'website',
        'knowledge',
        'website_parameterized_snippet'
    ],
    "data": [
        'data/cron.xml',
        'data/themes.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
}
