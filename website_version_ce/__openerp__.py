# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Website Versioning',
    'category': 'Website',
    'summary': 'Allow to save all the versions of your website and allow to perform AB testing.',
    'version': '9.0.1.0.0',
    'description': """
OpenERP Website CMS
===================

        """,
    'depends': ['website', 'marketing', 'google_account', 'mail'],
    'author': 'Odoo S.A., Clouder SASU, Odoo Community Association (OCA)',
    'installable': True,
    'data': [
        'security/ir.model.access.csv',
        'views/website_version_ce_templates.xml',
        'views/marketing_view.xml',
        'views/website_version_ce_views.xml',
        'views/res_config.xml',
        'data/data.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'application': False,
}
