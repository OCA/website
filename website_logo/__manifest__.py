# -*- coding: utf-8 -*-
# Copyright 2015 Agile Business Group - Lorenzo Battistini
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - David Vidal
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': 'Website logo',
    'summary': 'Website company logo',
    'version': '10.0.1.0.0',
    'category': 'Website',
    'author': "Agile Business Group, "
              "LasLabs, "
              "Tecnativa, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/res_config_view.xml',
        'views/website_view.xml',
        'views/website_templates.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
}
