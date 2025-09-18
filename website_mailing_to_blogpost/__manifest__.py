# Copyright 2025 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website - Mass Mailing to Blogpost",
    "category": "Email Marketing",
    "summary": "Converts (marketing) newsletter to blogpost",
    "license": "AGPL-3",
    "version": "16.0.1.0.0",
    "author": "Onestein, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": [
        "mass_mailing",
        "website",
        "website_blog",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/general_newsletter_tag.xml",
        "wizards/newsletter_to_blogpost_wizard.xml",
        "views/mailing_mailing.xml",
    ],
}
