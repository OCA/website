# -*- coding: utf-8 -*-
{
    'name': "Google Tag Manager",

    'summary': """
        Easily add Google Tag Manager""",

    'description': """
        This module adds a field Google Tag Manager
        to the config of website.
        When this field has been given a value,
        the template website.layout will receive the
        google tag manager code with the given tag_id.
        This will be the first tag inside the <body> tag.
        Unless you are logged in, then the
        website-top-navbar will be the first tag
    """,

    'author': "Sonny@CatsAndDogs.com",
    'website': "http://www.catsanddogs.com",
    'category': 'Website',
    'version': '0.1',

    'depends': ['website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}
