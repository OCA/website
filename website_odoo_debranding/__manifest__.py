# Copyright 2016 Tecnativa, S.L. - Vicent Cubells
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Remove Odoo Branding from Website",
    "version": "15.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "LGPL-3",
    "category": "Website",
    "depends": ["website"],
    "data": ["templates/disable_odoo.xml"],
    "installable": True,
    "post_init_hook": "post_init_hook",
}
