# Copyright 2020 Trey - Antonio González <antonio@trey.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Cookiebot',
    'summary': 'Cookiebot integration',
    'category': 'Website',
    'version': '13.0.1.0.0',
    'author': 'Trey (www.trey.es), Odoo Community Association (OCA)',
    'website': 'https://www.trey.es',
    'license': 'AGPL-3',
    'depends': [
        'portal',
        'website',
    ],
    'data': [
        'data/cookies_policy.xml',
        'views/portal_template.xml',
        'views/res_config_settings_views.xml',
        'views/web_template.xml',
    ],
}
