# Copyright 2016-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Form - ReCaptcha",
    "summary": "Provides a ReCaptcha field for Website Forms",
    "version": "13.0.1.0.2",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "LasLabs, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": ["website_form"],
    "data": ["views/assets.xml", "views/website_config_settings.xml"],
    "qweb": ["static/src/xml/recaptcha.xml"],
    "images": ["static/description/website_form_recaptcha.jpg"],
}
