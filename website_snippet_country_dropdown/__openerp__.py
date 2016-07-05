# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Website Snippet Country Dropdown Code",
    "summary": "Allow to select country in a dropdown",
    "version": "8.0.1.1.0",
    "category": "Website",
    "website": "http://www.tecnativa.com",
    "author": "Tecnativa, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    'qweb': ['static/src/xml/*.xml'],
    "data": [
        "views/assets.xml",
        "views/snippets.xml",
    ],
    "demo": [
        "demo/pages.xml",
    ],
}
