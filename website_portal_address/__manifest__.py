# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2016-Today Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)
{
    "name": "Contact's Address Manager In Website Portal",
    "summary": "Contact's Address Manager In Website Portal",
    "version": "12.0.1.0.0",
    "category": "Portal",
    "author": """Serpent Consulting Services Pvt. Ltd.,
                Agile Business Group,
                Odoo Community Association (OCA)""",
    "website": "https://github.com/OCA/website"
               "/tree/12.0/website_portal_address",
    "license": "AGPL-3",
    "depends": [
        "website_portal_contact",
    ],
    "data": [
        "views/assets.xml",
        "views/contact_address.xml",
        "views/layout.xml",
    ],
    "installable": True,
}
