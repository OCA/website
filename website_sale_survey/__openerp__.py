# -*- coding: utf-8 -*-
# Copyright 2016 Jamotion GmbH
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
#    Created by angel.moya on 01.09.2016.
#
{
    "name": "Website Sale Survey",
    "summary": "Survey for Online Sales",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://jamotion.ch",
    "author": "Jamotion GmbH, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    'depends': [
        'website_sale',
        'survey'
    ],
    'data': [
        'views/template.xml',
        'views/survey_view.xml',
    ]
}
