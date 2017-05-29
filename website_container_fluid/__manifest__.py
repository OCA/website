# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Snippet container width type chooser",
    "summary": "Let you choose between fixed or fluid containers",
    "version": "10.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",

    "website": "https://www.tecnativa.com",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",

    "application": False,
    'installable': True,

    "depends": [
        "website",
    ],
    "data": [
        "templates/snippets.xml",
    ],
    "demo": [
        "demo/pages.xml",
    ],
}
