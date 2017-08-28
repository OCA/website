# -*- coding: utf-8 -*-
# Copyright 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Website Multi Theme",
    "summary": "Support different theme per website",
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://www.tecnativa.com",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/website_config_settings_view.xml",
        "data/themes_bootswatch.xml",
        "data/themes_private.xml",
        "templates/assets.xml",
        "templates/patterns.xml",
    ],
    "demo": [
        "demo/pages.xml",
        "demo/themes.xml",
    ],
    "external_dependencies": {
        "bin": [
            "lessc",
            "sass",
            "scss",
        ],
    },
}
