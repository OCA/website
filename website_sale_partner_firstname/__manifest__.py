# Copyright 2023 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Contact Lastname",
    "version": "15.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Sygel Technology," "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_account_fiscal_position_partner_type",
        "partner_firstname",
    ],
    "data": [
        "views/templates.xml",
        "views/auth_signup_login_templates.xml",
        "views/portal_templates.xml",
    ],
}
