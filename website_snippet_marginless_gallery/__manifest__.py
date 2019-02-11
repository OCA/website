# Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Marginless Gallery Snippet",
    "summary": "Add a snippet to have a marginless image gallery",
    "version": "12.0.1.0.0",
    "category": "Website",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/website",
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
}
