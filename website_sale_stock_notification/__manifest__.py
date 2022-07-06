{
    "name": "Website Sale Stock Notification ",
    "category": "Website",
    "version": "15.0.1.0.0",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "author": "Nitrokey GmbH," "Odoo Community Association (OCA)",
    "summary": """
This module adds a new option to products to control how (almost) empty stock
is displayed in the online shop. The new option is: "show inventory below a"
threshold, sell regardless and show product-specific notification for empty
"stock"
""",
    "depends": [
        "website_sale_stock",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_sale_stock_notification/static/src/js/website_sale_stock.js",
        ],
        "web.assets_qweb": [
            "website_sale_stock_notification/static/src/xml/*.xml",
        ],
    },
}
