# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Field AutoComplete Related",
    "summary": 'Extends website autocomplete field to allow updates of '
               'related fields.',
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_field_autocomplete",
    ],
    "data": [
        'views/assets.xml',
    ],
    'demo': [
        'demo/field_autocomplete_demo.xml',
    ]
}
