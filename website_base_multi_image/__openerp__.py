# -*- coding: utf-8 -*-
# © 2016 Sergio Teruel <sergio.teruel@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': "Website Base Multi Image",
    'summary': "Show multi images data in frontend",
    'category': 'Website',
    'version': '9.0.1.0.0',
    'depends': [
        'website',
        'base_multi_image',
    ],
    'data': [
        'views/assets.xml',
        'views/layout.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'author': 'Tecnativa',
    'website': 'http://www.tecnativa.com',
    'license': 'LGPL-3',
    'installable': True,
}
