# -*- coding: utf-8 -*-
# Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cookie Notice',
    'summary': 'Show cookie notice according to cookie law',
    'version': '9.0.1.0.0',
    'category': 'Website',
    'author': "Agile Business Group, Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/assets_frontend_template.xml',
        'views/res_company_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
