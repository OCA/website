# Copyright 2013-2017 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website Menu By User Display',
    'version': '12.0.1.0.0',
    'author': 'Savoir-faire Linux,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'license': 'AGPL-3',
    'category': 'Website',
    'summary': 'Allow to manage the display of website.menus',
    'depends': [
        'website',
    ],
    'data': [
        'views/website_menu.xml',
    ],
    'installable': True,
}
