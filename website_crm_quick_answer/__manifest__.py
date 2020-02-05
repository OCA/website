# Copyright 2016 Tecnativa - Jairo Llopis
# Copyright 2017 Tecnativa - David Vidal
# Copyright 2019 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Quick answer for website contact form",
    "summary": "Add an automatic answer for contacts asking for info",
    'category': 'Website',
    'version': '12.0.1.1.0',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website_crm',
        'base_automation',
    ],
    'data': [
        "data/base_automation_data.xml",
    ],
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
}
