# -*- coding: utf-8 -*-
# This file is part of OpenERP. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Website Menu Multilanguage',
    'version': '0.1',
    'author': 'Versada UAB',
    'category': 'Website',
    'website': 'http://www.versada.lt',
    'description': """
Enables specifying languages for Website Menus.

When website is viewed in specific language only Menus in that language will
be displayed.

TODO:
* Restrict direct URL access for pages of unspecified language
* Proper sitemap.xml generation
* Solve exceptional Use Cases (no language defined; only one language available etc.)
* Theme compatibility
* Tests
    """,
    'depends': [
        'website',
    ],
    'data': [
        'view/website.xml',
    ],
    'update_xml': [],
    'installable': True,
    'application': False,
}
