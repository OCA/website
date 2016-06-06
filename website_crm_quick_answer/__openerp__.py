# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Jairo Llopis
# See README.rst file on addon root folder for more details

{
    'name': "Quick answer for website contact form",
    "summary": "Add an automatic answer for contacts asking for info",
    'category': 'Customer Relationship Management',
    'version': '8.0.1.0.0',
    'depends': [
        'marketing_campaign',
        'website_crm',
    ],
    'data': [
        "data/automation.xml",
    ],
    'author': 'Antiun Ingeniería S.L., '
              'Odoo Community Association (OCA)',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
