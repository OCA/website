# Copyright 2022 Odoo S. A.
# Copyright 2022 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

{
    "name": "Plausible analytics",
    "version": "14.0.1.0.1",
    "author": "Odoo S.A., ForgeFlow, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "maintainers": ["LoisRForgeFlow"],
    "license": "LGPL-3",
    "category": "Website",
    "summary": "Track website users using plausible",
    "depends": ["website"],
    "data": [
        "views/website_config_settings.xml",
        "views/templates.xml",
    ],
    "installable": True,
}
