#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website URL Exclusion",
    "summary": "Exclude URLs from the website sitemap",
    "version": "12.0.1.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website"
               "/tree/12.0/website_url_sitemap_exclusion",
    "author": "TAKOBI, "
              "Odoo Community Association (OCA)",
    "depends": [
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/website_views.xml",
    ],
}
