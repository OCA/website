# -*- coding: utf-8 -*-
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Cookie notice',
    'summary': 'Show cookie notice according to cookie law',
    'version': '9.0.1.0.0',
    'category': 'Website',
    'author': "Agile Business Group, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website_legal_page',
    ],
    'data': [
        'views/website.xml',
    ],
    'installable': True,
    'auto_install': False,
}
