# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Portal Pager Size",
    "summary": "Adds a configurable page size selector to portal pages, "
    "allowing users to control the number of records displayed "
    "per page via the portal pager.",
    "version": "16.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "XXP, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["portal"],
    "data": [
        "data/ir_config_parameter_data.xml",
        "templates/portal_templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "portal_pager_size/static/src/scss/portal_pager_size.scss",
            "portal_pager_size/static/src/js/portal_pager_size.esm.js",
        ],
    },
    "installable": True,
}
