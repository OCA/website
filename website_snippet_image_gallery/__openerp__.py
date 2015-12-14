# -*- coding: utf-8 -*-
# © 2015 Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Snippet Image Gallery',
    'category': 'Website',
    'author': 'Serpent Consulting Services Pvt. Ltd.',
    "author": """Serpent Consulting Services Pvt. Ltd.,
                 Odoo Community Association (OCA)""",
    'website': 'http://www.serpentcs.com',
    'summary': 'Adds image gallery in website.',
    'version': '8.0.1.0.0',
    'depends': [
        'website',
    ],
    'data': [
        'views/assets.xml',
        'views/image-gallery-snippet.xml',
    ],
    'installable': True,
    'auto_install': False,
}
