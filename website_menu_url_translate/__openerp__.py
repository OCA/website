# -*- coding: utf-8 -*-
# Copyright 2017 initOS GmbH. <http:/www.initos.com>
# Copyright 2017 GYB IT SOLUTIONS <http:/www.gybitsolutions.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Website Menu URL Translation",
    'category': "Website",
    'website': "www.gybitsolutions.com",
    'version': "8.0.1.0.0",
    'description': '''
    Module has functionality of translate website URL for different Languages.
    ''',
    'author': "GYB IT SOLUTIONS,"
              "initOS GmbH.,"
              "Odoo Community Association (OCA)",
    'depends': ['website'],
    'data': [
        'views/website_contentMenu.xml',
    ],
    'installable': True,
    'application': False,
}
