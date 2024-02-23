{
    "name": "Website Default Code Product",
    "category": "Website",
    "version": "16.0.1.0.0",
    "website": "https://github.com/OCA/website",
    "author": "ForgeFlow, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "depends": ["website_sale"],
    "data": [
        "views/website_default_code_product_views.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "website_default_code_product/static/src/scss/website_default_code_product.scss",
        ],
    },
    "installable": True,
}
