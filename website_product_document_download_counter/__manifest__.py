# Copyright 2025 Cetmix OÜ
# License LGPL-3.0 or later (https://www.gnu.org/licenses/LGPL).

{
    "name": "Website Product Document Download Counter",
    "summary": "Counts the product document downloads from the website.",
    "version": "18.0.1.0.0",
    "category": "Website",
    "author": "Cetmix OÜ, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "LGPL-3",
    "depends": ["website_sale"],
    "data": [
        "views/product_document_views.xml",
        "views/documents.xml",
    ],
    "installable": True,
    "application": False,
}
