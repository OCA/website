# -*- coding: utf-8 -*
# © 2015 Agile Business Group sagl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Logo',
    'summary': 'Website Company Logo',
    'version': '9.0.1.0.0',
    'category': 'Website',
    'author': "Agile Business Group, "
              "Antiun Ingeniería S.L., "
              "LasLabs, "
              "Odoo Community Association (OCA)",
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/res_config.xml',
        'views/website.xml',
        'views/website_templates.xml',
    ],
    'installable': True,
    'auto_install': False,
}
