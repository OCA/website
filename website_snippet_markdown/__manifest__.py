# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Website Markdown Snippet',
    'category': 'Website',
    'version': '10.0.1.0.0',
    'author': 'Onestein', 'Odoo Community Association (OCA)",
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': [
        'website',
        'web'
    ],
    'data': [
        'templates/assets.xml',
        'templates/snippets.xml',
    ],
    'qweb': [
        'static/src/xml/website_snippet_markdown.xml',
    ],
}
