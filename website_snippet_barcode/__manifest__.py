# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Website Snippet - Barcode",
    "summary": "Generates barcodes for advertising content",
    "version": "10.0.1.0.0",
    "category": "Website",
    "website": "https://laslabs.com/",
    "author": "LasLabs, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "report",
        "website",
    ],
    "data": [
        "templates/assets.xml",
        "templates/snippet_template.xml",
    ],
    "demo": [
        "demo/assets_demo.xml",
        "demo/website_snippet_barcode_demo.xml",
    ],
}
