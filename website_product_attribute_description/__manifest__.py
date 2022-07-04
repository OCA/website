{
    "name": "Website Attribute Description",
    "version": "15.0.1.0.0",
    "category": "Website",
    "author": "ERP Harbor Consulting Services,"
    "Nitrokey GmbH,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "summary": """
    Website Attribute Description
    This module adds the information icon next to the attribute name in the
    website and display the related description on mouse hover.
     """,
    "depends": ["product_attribute_description", "website_sale"],
    "data": [
        "views/template.xml",
    ],
    "assets": {
        "website.frontend_assets": [
            "/product_attribute_description/static/src/css/tooltip.css",
            "/product_attribute_description/static/src/js/tooltip.js",
        ],
    },
    "license": "AGPL-3",
    "installable": True,
}
