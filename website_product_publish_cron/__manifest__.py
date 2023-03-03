# Copyright 2023 Quartile Limited
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Product Publish Cron",
    "category": "Website",
    "version": "15.0.1.0.0",
    "author": "Quartile Limited, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["website_sale"],
    "data": [
        "data/product_publish_cron.xml",
        "views/product_template_views.xml",
    ],
    "installable": True,
}
