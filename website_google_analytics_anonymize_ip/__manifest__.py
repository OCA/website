# Copyright 2020 CodeNext
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Google Analytics Anonymize IP',
    'summary': """
        Enabling the IP Anonymization feature in Google Analytics""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'CodeNext,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website'
    ],
    'data': [
        'views/res_config_settings.xml',
        'views/website_templates.xml',
    ]
}
