# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Blog Title Image',
    'category': 'Website',
    'summary': 'Enables adding title image to blogpost.',
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'description': """
        """,
    'author': 'Onestein',
    'depends': [
        'website_blog'
    ],
    'data': [
        'views/website_blog_templates.xml',
        'views/blog_post_view.xml'
    ],
    'installable': True,
}
