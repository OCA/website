# Copyright 2016-2017 LasLabs Inc.
# Copyright 2019 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website CRM - ReCaptcha",
    "summary": 'Provides a ReCaptcha validation in Website Contact Form',
    "version": "12.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "LasLabs, Tecnativa, Odoo Community Association (OCA)",
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
    'images': [
        'static/description/website_crm_recaptcha.jpg',
    ],
}
