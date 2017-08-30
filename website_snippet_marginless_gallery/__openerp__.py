# -*- coding: utf-8 -*-
{
    "name": "Marginless Gallery Snippet",
    "summary": "Add a snippet to have a marginless image gallery",
    "version": "9.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "website": "https://odoo-community.org/project/website-maintainers-79",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    "application": False,
    "installable": True,
    "images": [
        "images/marginless_gallery.png",
    ],
    "depends": [
        "website",
    ],
    "data": [
        "views/assets.xml",
        "views/snippets.xml",
    ],
    "demo": [
        "demo/assets.xml",
    ],
}
