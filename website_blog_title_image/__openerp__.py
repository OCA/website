# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Blog Title Image',
    'category': 'Website',
    'summary': 'Enables adding title image to blogpost.',
    'version': '1.0',
    'description': """
        """,
    'author': 'Onestein',
    'depends': ['website', 'website_blog'],
    'data': [
        'views/assets.xml',
        'views/website_blog_templates.xml'
    ],
    'installable': True,
}