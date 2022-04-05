# Copyright 2016-2017 LasLabs Inc.
# Copyright 2019 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website CRM - ReCaptcha",
    "summary": "Provides a ReCaptcha validation in Website Contact Form",
    "version": "13.0.1.0.2",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "LasLabs, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "uninstall_hook": "uninstall_hook",
    "depends": ["website_crm", "website_form_recaptcha"],
    "data": ["data/ir_model_data.xml"],
    "images": ["static/description/website_crm_recaptcha.jpg"],
}
