# -*- coding: utf-8 -*-
# © 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Excerpt + Image in Blog",
    "summary": "New layout for blog summary, including an excerpt and image",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://grupoesoc.es",
    "author": "Grupo ESOC Ingeniería de Servicios, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "images": [
        "images/style-default.png",
    ],
    "depends": [
        "website_blog",
        "html_image_url_extractor",
        "html_text",
    ],
    "data": [
        "views/assets.xml",
        "views/blog.xml",
    ],
}
