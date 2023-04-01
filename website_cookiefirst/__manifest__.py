# Copyright 2021 Studio73 - Ioan Galan <ioan@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Cookiefirst",
    "summary": "Cookiefirst integration",
    "category": "Website",
    "version": "14.0.1.1.0",
    "author": "Studio73, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["portal", "website"],
    "data": [
        "data/cookies_policy.xml",
        "views/portal_template.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
}
