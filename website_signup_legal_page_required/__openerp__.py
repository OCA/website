# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Require accepting legal terms",
    "summary": "Force the user to accept the legal terms to open an account",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_legal_page",
    ],
    "data": [
        "views/pages.xml",
    ],
}
