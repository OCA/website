# Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Website Legal Page",
    "category": "Website",
    "version": "15.0.1.0.0",
    "depends": ["website"],
    "data": [
        "views/reusable_templates.xml",
        "views/website_legal_main_page.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "/website_legal_page/static/src/css/website_legal_page.scss"
        ]
    },
    "author": "Tecnativa, "
    "LasLabs, "
    "Nicolas JEUDY, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "post_init_hook": "post_init_hook",
}
