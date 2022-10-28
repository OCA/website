# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Umami analytics",
    "version": "16.0.1.0.0",
    "author": "Yigit Budak, Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Privacy-focused web analytics with Umami",
    "depends": ["website"],
    "data": [
        "views/website_config_settings.xml",
        "views/website.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
