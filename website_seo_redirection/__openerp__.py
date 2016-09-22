# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website SEO Redirection",
    "summary": "Redirect any controller to the URL of your dreams",
    "version": "8.0.1.1.0",
    "category": "Website",
    "website": "https://tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/website_seo_redirection_view.xml",
    ],
    "demo": [
        "demo/website_seo_redirection_demo.xml",
    ],
}
