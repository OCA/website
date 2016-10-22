# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Field - AutoComplete",
    "summary": 'Provides an autocomplete field for Website on any model',
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "website",
    ],
    "data": [
        'views/assets.xml',
    ],
    'demo': [
        'demo/field_autocomplete_demo.xml',
    ]
}
