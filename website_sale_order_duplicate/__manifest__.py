# Copyright 2019 Trey
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Website Sale Order Duplicate",
    "summary": "Duplicate order and set it as current cart",
    "category": "Website",
    "version": "16.0.1.0.0",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": [
        "portal",
        "sale",
        "website_sale",
    ],
    "data": [
        "views/portal_my_orders_inherit_views.xml",
        "views/portal_my_quotations_inherit_views.xml",
    ],
}
