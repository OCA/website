# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Form - ReCaptcha",
    "summary": 'Provides a ReCaptcha field for Website Forms',
    "version": "10.0.1.0.1",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "website_form",
    ],
    "data": [
        "data/ir_config_parameter_data.xml",
        'views/assets.xml',
    ],
}
