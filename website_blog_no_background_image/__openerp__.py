# -*- coding: utf-8 -*-
# © 2015 Therp B.V, Giovanni Francesco Capalbo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Optional Background image for Blog Posts",
    "summary": "Choose how to display Blog Post headers",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://odoo-community.org/",
    "author": "Therp BV,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        'website_blog'
    ],
    "data": [
        "views/views.xml",
        "views/templates.xml",
    ],
    "css": [
        "static/src/css/website_blog_nobkimage.css",
    ],
    "auto_install": False,
    "installable": True,
    "application": False,
}
