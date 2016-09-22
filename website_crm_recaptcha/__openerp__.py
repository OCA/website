# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website CRM - ReCaptcha",
    "summary": 'Provides a ReCaptcha validation in Website Contact Form',
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_crm",
        'website_form_recaptcha',
    ],
    "data": [
        'views/website_crm_template.xml',
    ],
}
