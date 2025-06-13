# Copyright (C) 2024 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Product Document Download Counter",
    "summary": "Cuenta las descargas de documentos de productos desde el website.",
    "version": "18.0.1.0.0",
    "category": "Website",
    "author": "Cetmix OÜ,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["website", "product", "website_sale"],
    "data": [
        "views/product_document_views.xml",
        "views/website_product_document_download_counter_views.xml",
    ],
    "installable": True,
    "application": False,
}
