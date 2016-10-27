# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Website Snippet - Data Slider",
    "summary":
        "Abstract data slider for use on website."
        "  Primary use (and default implementation) is product slider.",
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website",
    ],
    "data": [
        "views/assets.xml",
        'views/snippet_template.xml',
    ],
    "demo": [
        "demo/data_slider_demo.xml",
    ],
}
