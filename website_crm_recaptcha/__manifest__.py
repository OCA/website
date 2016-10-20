# -*- coding: utf-8 -*-
# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website CRM - ReCaptcha",
    "summary": 'Provides a ReCaptcha validation in Website Contact Form',
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "website_crm",
        'website_form_recaptcha',
    ],
    "data": [
        "data/ir_model_data.xml",
        'views/website_crm_template.xml',
    ],
}
