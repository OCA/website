# -*- coding: utf-8 -*-
# Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website logo',
    'summary': 'Website company logo',
    'version': '8.0.1.0.0',
    'category': 'Website',
    'author': "Agile Business Group,Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/company_view.xml',
        'views/website_templates.xml',
    ],
    'qweb': [
    ],
    'installable': False,
    'auto_install': False,
}
