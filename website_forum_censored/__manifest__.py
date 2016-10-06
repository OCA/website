# -*- coding: utf-8 -*-
# © 2016 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Forum Censorship',
    'category': 'Website',
    'version': '9.0.1.0.0',
    'author': 'Onestein, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': ['website_forum'],
    'data': [
        'security/ir.model.access.csv',
        'views/forum_censored_phrase.xml',
        'menuitems.xml'
    ],
    'summary': "Block phrases entered in forum posts and comments.",
    'installable': False,
}
