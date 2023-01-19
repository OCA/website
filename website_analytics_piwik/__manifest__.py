# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Piwik analytics",
    "version": "14.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Track website users using piwik",
    "depends": [
        "website",
    ],
    "data": [
        "views/res_config_settings.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
