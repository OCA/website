# -*- encoding: utf-8 -*-
{
    "name": "Marginless Gallery Snippet",
    "summary": "Add a snippet to have a marginless image gallery",
    "version": "8.0.1.0.1",
    "category": "Website",
    "license": "AGPL-3",

    "website": "https://odoo-community.org/project/website-maintainers-79",
    "author": "Grupo ESOC, Odoo Community Association (OCA)",

    "application": False,
    "installable": True,

    "depends": [
        "website",
    ],
    "data": [
        "views/assets.xml",
        "views/snippets.xml",
    ],
}
