# Copyright 2021 Lorenzo Battistini @ TAKOBI
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Newsletter Subscribe Button - Privacy Policy",
    "summary": "Users must accept privacy policy in order to subscribe to newsletters",
    "version": "12.0.1.0.0",
    "development_status": "Beta",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "TAKOBI, Odoo Community Association (OCA)",
    "maintainers": ["eLBati"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "website_mass_mailing",
        "website_legal_page",
    ],
    "data": [
        "views/assets.xml",
        "views/snippets_templates.xml",
    ],
}
