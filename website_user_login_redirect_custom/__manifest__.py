# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website User Login Redirect Custom",
    "summary": "Redirect website/portal user to custom URL after login or signup",
    "version": "18.0.1.0.0",
    "category": "Website",
    "author": "Cetmix OÜ, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "depends": ["website"],
    "data": [
        "data/ir_config_parameter_data.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
}
