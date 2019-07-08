# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Extendible global website search",
    "version": "10.0.1.0.0",
    "author": "Therp BV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": """Adds a snippet that will search for keywords globally in
                  website""",
    "depends": [
        "website",
    ],
    "data": [
        "views/snippets.xml",
        "views/templates.xml",
    ],
}
