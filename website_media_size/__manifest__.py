# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Show Media Size',
    'summary': 'This module shows the size of media in the media selector',
    'category': 'Website',
    'version': '12.0.1.0.0',
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
        'static/src/xml/website_media_size.xml'
    ],
}
