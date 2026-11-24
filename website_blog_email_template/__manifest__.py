# Copyright 2025 Escodoo <https://escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Blog Email Template",
    "summary": "Allow configuring custom email template for new blog posts",
    "version": "18.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "maintainers": ["marcelsavegnago"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website_blog"],
    "data": [
        "data/mail_template_data.xml",
        "views/website_blog_views.xml",
    ],
}
