# Copyright 2015-2016 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
# Copyright 2019 Tecnativa - Cristina Martin R.
# Copyright 2022 Tecnativa - Guillermo Gallego <guillermo.gallego@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Big Buttons Snippet",
    "summary": "A snippet that adds two big buttons",
    "version": "15.0.1.1.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Grupo ESOC Ingeniería de Servicios, S.L.U., "
    "Tecnativa, "
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": ["website"],
    "data": ["templates/snippets.xml"],
    "assets": {
        "web.assets_frontend": [
            "/website_snippet_big_button/static/src/scss/website_snippet_big_button.scss"
        ]
    },
}
