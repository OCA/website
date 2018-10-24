# -*- coding: utf-8 -*-
{
    'name': 'Slides',
    'version': '8.0.2.0.1',
    'license': 'LGPL-3',
    'summary': 'Share and Publish Videos, Presentations and Documents',
    'category': 'Website',
    'author': "Odoo SA, "
              "Incaser Informatica - Sergio Teruel, "
              "Odoo Community Association (OCA)",
    'website': 'https://github.com/OCA/website',
    'depends': ['website',
                'website_mail',
                'marketing'],
    'data': [
        'views/res_config.xml',
        'views/website_slides.xml',
        'views/website_slides_embed.xml',
        'views/website_slides_backend.xml',
        'views/website_templates.xml',
        'data/website_slides_data.xml',
        'security/ir.model.access.csv',
        'security/website_slides_security.xml'
    ],
    'demo': [
        'data/website_slides_demo.xml'
    ],
    'installable': True,
    'application': True,
}
