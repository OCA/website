# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "website_blog_layout_options",
    "version": "8.0.1.0.0",
    "author": "Therp BV"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "Adds options for the blogpost and blog layouts",
    "depends": [
        'website_blog'
    ],
    "data": [
        'views/templates.xml',
        'views/teaser.xml',
        'views/views.xml',
    ],
    "css": [
        "static/src/css/website_blog_layout_options.css",
    ],
    "pre_init_hook": False,
    "post_init_hook": False,
    "uninstall_hook": False,
    "auto_install": False,
    "installable": True,
    "application": False,
    "external_dependencies": {
        'python': [],
    },
}
