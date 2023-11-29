# -*- coding: utf-8 -*-

{
    'name': 'Website Cookie Consent',
    'version': '8.0.1.0.0',
    'author': "Therp BV,Odoo Community Association (OCA)",
    'maintainer': 'Therp BV',
    'website': 'https://www.therp.nl',
    'category': 'Website',
    'depends': [
        'website',
    ],
    'summary': """This module configures cookie consent for website""",
    'data': [
        'views/assets.xml',
        'data/website_cookieconsent_data.xml'
    ],
    'installable': True,
    'license': 'LGPL-3',
}
