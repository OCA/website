# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Theme Flexible',
    'summary': 'Theme Flexible is exceptionally configurable.',
    'category': 'Theme',
    'version': '11.0.1.0.0',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website'
    ],
    'data': [
        'views/res_config_settings_view.xml',

        'data/theme_flexible_data.xml',
        'data/website_data.xml',

        'templates/assets.xml',
        'templates/theme_customize.xml',
        'templates/color_picker.xml',
        'templates/options/fonts.xml',
        'templates/options/colors.xml',
        'templates/options/menu.xml',
        'templates/options/layout.xml',
        'templates/options/anchor.xml',

        'security/ir.model.access.csv'
    ]
}
