# Copyright 2020 Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website JS Below The Fold Payment',
    'category': 'Website',
    'version': '12.0.1.0.0',
    'author': 'Druidoo, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website_js_below_the_fold',
        'payment',
    ],
    'data': [
        'templates/templates.xml'
    ],
    'auto_install': True,
}
