# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Snippet Presets',
    'summary': 'This module allows the user '
               'to save and restore presets of snippets.',
    'category': 'Website',
    'version': '11.0.1.0.0',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'website'
    ],
    'data': [
        'templates/assets.xml',
        'security/ir.model.access.csv'
    ],
    'qweb': [
        'static/src/xml/website_snippet_preset.xml'
    ],
    'installable': True,
}
