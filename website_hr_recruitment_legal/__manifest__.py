# Copyright 2019 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Legal acceptance checkbox for recruitment website form",
    "summary": "People must accept legal terms to apply for a job",
    "version": "11.0.1.0.0",
    "development_status": "Alpha",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_hr_recruitment",
        "website_legal_page",
    ],
    "data": [
        "templates/apply.xml",
    ],
}
