{
    "name": "Nitrokey Website Sale Stock - Website Delivery Information",
    "category": "Website",
    "version": "15.0.1.0.0",
    "license": "AGPL-3",
    "author": "Nitrokey GmbH, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "summary": """
This module adds a new option to products to control how (almost) empty stock
is displayed in the online shop. The new option is: "show inventory below a"
threshold, sell regardless and show product-specific notification for empty
"stock"
""",
    "depends": [
        "website_sale_stock",
        "website_sale",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/res_config_settings_views.xml",
        "views/templates.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "nitrokey_website_sale_stock/static/src/js/website_sale_stock.js",
        ],
        "web.assets_qweb": [
            "nitrokey_website_sale_stock/static/src/xml/*.xml",
        ],
    },
}
