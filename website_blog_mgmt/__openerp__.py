# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    'name': 'Website blog Management',
    'version': '9.0.1.0.0',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'http://www.acsone.eu',
    'license': 'AGPL-3',
    'category': 'Website',
    'depends': [
        'website_blog',
    ],
    'data': [
        'data/website_blog_mgmt_data.xml',
        'views/website_blog_views.xml',
        'views/website_blog_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
    'post_init_hook': 'post_init',
}
