# Copyright 2024 Christopher Ormaza <chris.ormaza@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website WhatsApp Dynamic Message",
    "version": "17.0.1.0.0",
    "category": "Website",
    "license": "AGPL-3",
    "author": "Christopher Ormaza, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website_whatsapp",
        "website_sale",
    ],
    "data": [
        "templates/website.xml",
    ],
    "installable": True,
    "auto_install": False,
}
