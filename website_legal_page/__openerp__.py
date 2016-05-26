# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
# © 2015 Antonio Espinosa <antonioea@antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': "Website Legal Page",
    'description': 'Add legal information, such as privacy policy',
    'category': 'Website',
    'version': '9.0.1.0.0',
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
              'LasLabs Inc, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
