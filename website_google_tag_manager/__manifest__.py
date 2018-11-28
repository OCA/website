# Copyright 2016 ABF OSIELL <http://osiell.com>
# Copyright 2018 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Google Tag Manager Support",
    "version": "11.0.1.0.0",
    "author": "ABF OSIELL, Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "summary": "Add support for Google Tag Manager",
    "depends": [
        'website',
    ],
    "data": [
        "views/res_config_settings_view.xml",
        "views/website_views.xml",
        'views/website_templates.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
}
