{
    "name": "First & Last Name at Checkout",
    "summary": "Separate first and last name fields at checkout and portal",
    "author": "Aaron Ngu, Odoo Community Association (OCA)",
    "category": "Website/Website",
    "version": "18.0.1.0.0",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "images": [],
    "depends": ["website_sale", "partner_firstname"],
    "data": [
        "data/res_partner_data.xml",
        "views/templates.xml",
    ],
}
