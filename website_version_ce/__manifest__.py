# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Website Versioning',
    'category': 'Website',
    'summary': 'Allow webpages versions and A/B testing.',
    'version': '10.0.1.0.0',
    'depends': ['website', 'google_account', 'mail'],
    'author': 'Odoo S.A., Clouder SASU, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/website_version_ce_templates.xml',
        'views/marketing_view.xml',
        'views/website_version_ce_views.xml',
        'views/base_config_settings.xml',
        'data/data.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': False,
}
