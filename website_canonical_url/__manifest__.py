# -*- coding: utf-8 -*-
# © initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Website Canoncial URL",
    'summary': "Canonical URL in Website Headers",
    'author': "initOS GmbH, Tecnativa, Odoo Community Association (OCA)",
    'website': "http://www.initos.com",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'installable': True,
    'depends': [
        'website',
    ],
    'data': [
        'views/templates.xml',
    ],
    'demo': [
        'demo/pages.xml',
    ],
}
