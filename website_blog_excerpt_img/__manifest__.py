# Copyright 2016 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
# Copyright 2019 Tecnativa - Cristina Martin R.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Blog Post List Excerpt+Image Layout",
    "summary": "New layout for blog posts list, "
               "and autoselect social share image when no cover is selected",
    "version": "12.0.1.2.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Odoo Community Association (OCA), "
              "Tecnativa",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "images": [
        "images/style-default.png",
    ],
    "depends": [
        "website_blog",
        "html_image_url_extractor",
    ],
    "data": [
        "templates/blog.xml",
        "templates/snippets.xml",
    ],
}
