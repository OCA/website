# -*- coding: utf-8 -*-
{
    'name': "Google Tag Manager",

    'summary': """
        Easily add Google Tag Manager""",

    'description': """
        This module adds a field Google Tag Manager to the config of website.
        When this field has been given a value, the template website.layout will receive the
        google tag manager code with the given tag_id.
        This will be the first tag inside the <body> tag. Unless you are logged in, then the
        website-top-navbar will be the first tag
    """,

    'author': "Sonny@CatsAndDogs.com",
    'website': "http://www.catsanddogs.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}