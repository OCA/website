# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Anchor Smooth Scroll',
    'summary': 'Replace default behavior for internal links (anchor only) with'
               ' smooth scroll',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'website': 'https://github.com/OCA/website',
    'author': 'Tecnativa, '
              'LasLabs, '
              'Nicolas JEUDY, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website',
    ],
    "data": [
        "views/assets.xml",
    ],
    "demo": [
        "demo/pages.xml",
    ],
}
