# Copyright 2025 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website - Company Mastodon Link",
    "summary": "Display Company Mastodon Link on Website",
    "version": "18.0.1.0.0",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "category": "Website",
    "depends": [
        "website_social_media_link",
        "res_company_mastodon_link",
        # Mastodon Icon is present only
        # in more recent version
        "base_fontawesome",
    ],
    "data": ["views/view_website.xml"],
}
