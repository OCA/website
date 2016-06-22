# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Blog Post Title Image',
    'images': [],
    'category': 'Website',
    'version': '8.0.1.0.0',
    'author': 'ONESTEiN BV,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': ['website_blog'],
    'data': [
        'views/website_blog_templates.xml',
        'views/blog_post_view.xml'
    ],
    'summary': 'Enables adding title image to blogpost.',
    'installable': True,
    'auto_install': False,
    'application': False,
}
