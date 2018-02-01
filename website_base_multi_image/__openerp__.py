# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': "Website Base Multi Image",
    'summary': "Show multi images data in frontend",
    'version': '9.0.1.0.0',
    'category': 'Website',
    "website": "https://tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    'installable': True,
    'depends': [
        'website',
        'base_multi_image',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/layout.xml',
    ],
    'demo': [
        'demo/website_base_multi_image_demo.xml',
        'demo/pages.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
}
