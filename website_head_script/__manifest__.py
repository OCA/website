# Copyright 2021 Lorenzo Battistini @ TAKOBI
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
{
    "name": "Website head scripts",
    "summary": "Add custom scripts to <head> of website",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "data": [
        "views/website_views.xml",
        "security/ir.model.access.csv",
        "views/website_templates.xml",
    ],
}
