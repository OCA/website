# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Multiple Websites',
    'summary': 'This module makes it easier to manage multiple websites in one database.',
    'category': 'Website',
    'version': '11.0.1.0.0',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/oca/website',
    'depends': [
        'website'
    ],
    'data': [
        'views/website_view.xml',
        'views/website_page_view.xml',
        'views/website_menu_view.xml',
        'views/ir_ui_view_view.xml',

        'templates/assets.xml',
        'templates/user_navbar_templates.xml',
        
        'menuitems.xml'
    ],
    'qweb': [
        'static/src/xml/website_multi.xml'
    ]
}
