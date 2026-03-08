# -*- coding: utf-8 -*-
{
    'name': "First & Last Name at Checkout",
    'summary': "Separate first and last name fields at checkout and portal",
    'author': "Aaron Ngu",
    'category': 'Website/Website',
    'version': '18.0.1.0.0',
    'license': 'AGPL-3',
    'images': [],
    'depends': ['website_sale', 'partner_firstname'],
    'data': [
        'data/res_partner_data.xml',
        'views/templates.xml',
    ],
}
