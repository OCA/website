# -*- encoding: utf-8 -*-
{
    "name": "Snippet container width type chooser",
    "summary": "Let you choose between fixed or fluid containers",
    "version": "8.0.1.0.1",
    "category": "Website",
    "license": "AGPL-3",

    "website": "https://odoo-community.org/project/website-maintainers-79",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",

    "application": False,
    "installable": True,

    "depends": [
        "website",
    ],
    "data": [
        "views/assets.xml",
        "views/snippets.xml",
    ],
    "demo": [
        "demo/pages.xml",
    ],
}
