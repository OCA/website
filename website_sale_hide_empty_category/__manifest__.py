# Copyright 2017 LasLabs Inc. <https://laslabs.com/>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website Sale - Hide Empty Categories",
    "summary": "Hide any Product Categories that are empty",
    "version": "11.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_sale",
    ],
    "data": [
        "views/website_sale_templates.xml",
    ],
}
