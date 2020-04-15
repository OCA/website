# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Optimize Images on Website',
    'summary': 'This module allows the user to manually'
               ' apply compression and resize options on an image.',
    'category': 'Website',
    'version': '12.0.1.0.1',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website'
    ],
    'data': [
        'templates/assets.xml'
    ],
    'qweb': [
        'static/src/xml/website_adv_image_optimization.xml'
    ],
}
