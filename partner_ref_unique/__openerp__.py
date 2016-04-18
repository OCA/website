# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Partner unique reference",
    "summary": "Add an unique constraint to partner ref field",
    "version": "8.0.1.0.0",
    "category": "Customer Relationship Management",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    # 'auto_install':False,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "base",
    ],
    "data": [
        "views/res_company_view.xml",
    ],
    "demo": [
    ],
    "qweb": [
    ]
}
