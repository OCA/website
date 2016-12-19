# -*- coding: utf-8 -*-
# Copyright 2016 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Google Tag Manager",
    "version": "9.0.1.0.0",
    "author": "ABF OSIELL, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Add support for Google Tag Manager",
    "depends": [
        'website',
    ],
    "data": [
        "views/website_config_settings.xml",
        "views/website.xml",
        'views/templates.xml',
    ],
    "auto_install": False,
    'installable': True,
    "application": False,
}
