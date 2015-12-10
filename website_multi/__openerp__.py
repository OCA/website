# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Multi Website",
    "summary": "Build and manage multiple Websites",
    "version": "8.0.2.0.0",
    "category": "Website",
    "website": "http://www.odoo.com",
    "author": "OpenERP SA, "
              "Antiun Ingeniería S.L., "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website"
    ],
    "installable": True,
    "data": [
        "data/data.xml",
        "views/res_config.xml",
        "views/website_views.xml",
        "views/website_templates.xml",
    ],
    "demo": [
        "demo/website.xml",
        "demo/template.xml",
    ],
}
