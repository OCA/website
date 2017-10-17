# -*- coding: utf-8 -*-
# Copyright 2015 Antonio Espinosa <antonioea@antiun.com>
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Website Legal Page",
    'description': 'Add legal information, such as privacy policy',
    'category': 'Website',
    'version': '10.0.1.2.0',
    'depends': [
        'website',
    ],
    'data': [
        'views/reusable_templates.xml',
        'views/website_legal.xml',
        'views/website_privacy.xml',
        'views/website_terms.xml',
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Tecnativa, '
              'LasLabs, '
              'Odoo Community Association (OCA)',
    'website': 'https://www.tecnativa.com',
    'license': 'AGPL-3',
    'installable': True,
}
