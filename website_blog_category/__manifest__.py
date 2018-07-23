# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    'name': 'Website Blog - Categories',
    'version': '10.0.1.0.0',
    'category': 'Blog',
    'author': "LasLabs, Odoo Community Association (OCA)",
    'website': 'https://laslabs.com',
    'license': 'LGPL-3',
    'installable': True,
    'depends': [
        'website_blog',
    ],
    'data': [
        'views/blog_blog_view.xml',
        'views/blog_category_view.xml',
        'views/blog_post_view.xml',
        'templates/website_blog_template.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/assets_demo.xml',
        'demo/blog_category_demo.xml',
        'demo/blog_post_demo.xml',
    ],
}
