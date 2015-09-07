# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

{
    'name': "Optional validation of VAT via VIES",
    'category': 'Accounting',
    'version': '8.0.1.0.0',
    'depends': [
        'base_vat',
    ],
    'external_dependencies': {},
    'data': [
        'views/res_partner_view.xml',
    ],
    'qweb': [
    ],
    'js': [
    ],
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'demo': [],
    'test': [],
    'installable': True,
    # 'auto_install':False,
    # 'application':False,
}
