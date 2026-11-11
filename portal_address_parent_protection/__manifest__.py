# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Portal Address Parent Protection",
    "summary": "Prevent portal users from editing their parent company",
    "version": "19.0.1.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "maintainers": ["MarcGForgeFlow"],
    "application": False,
    "installable": True,
    "depends": ["portal"],
    "data": [
        "views/address_templates.xml",
    ],
}
