# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Matomo analytics",
    "version": "15.0.1.0.0",
    "author": "Onestein,Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Track website users using matomo",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website",
    ],
    "data": [
        "views/res_config_settings.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
