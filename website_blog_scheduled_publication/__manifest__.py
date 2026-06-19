# Copyright 2026 - TODAY, Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Blog Scheduled Publication",
    "summary": "Schedule blog posts publication date",
    "version": "18.0.1.0.0",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "maintainers": ["marcelsavegnago", "CristianoMafraJunior"],
    "license": "AGPL-3",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website_blog",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron.xml",
        "views/blog_post_views.xml",
        "wizard/blog_post_schedule_date_views.xml",
    ],
    "installable": True,
    "application": False,
}
