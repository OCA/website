# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# Copyright 2023 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Membership Gamification",
    "summary": "Show badges assigned to users on website",
    "version": "14.0.1.0.0",
    "category": "Website",
    "author": "Sygel, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "development_status": "Beta",
    "depends": ["gamification", "website_membership"],
    "data": [
        "wizard/gamification_badge_user_wizard.xml",
        "views/badge.xml",
        "views/res_partner_views.xml",
        "views/website_partner_template.xml",
    ],
}
