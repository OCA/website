# -*- coding: utf-8 -*-
# License AGPL-3: Antiun Ingenieria S.L. - Antonio Espinosa
# See README.rst file on addon root folder for more details

{
    'name': "Antiun Master common",
    'category': 'Personalization',
    'version': '8.0.1.0.0',
    'depends': [
        'antiun_backend_theme',
        'support_branding',
        'disable_openerp_online',
        'base_export_manager',
        'mass_editing',
        'auth_signup_verify_email',
        'instance_watermark',
        'web_sheet_full_width',
        'web_translate_dialog',
        'web_dialog_size',
        'web_tree_many2one_clickable',
        'web_m2x_options',
        'web_advanced_search_x2x',
        'web_searchbar_full_width',
        'mail_attach_existing_attachment',
        'mail_compose_select_lang',
        'mail_forward',
        'mail_full_expand',
        'mail_sent',
        'mail_mandrill',
    ],
    'external_dependencies': {},
    'data': [
        'data/support_branding.xml',
        'data/web_tree_many2one_clickable.xml',
        'data/web_m2x_options.xml',
    ],
    'author': 'Antiun Ingeniería S.L.',
    'website': 'http://www.antiun.com',
    'license': 'AGPL-3',
    'installable': True,
}
