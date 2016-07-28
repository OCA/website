# -*- coding: utf-8 -*-
# © 2016 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Blog tags cloud variable dimension",
    "version": "8.0.1.0.0",
    "author": "Therp BV,Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Website",
    "summary": "",
    "depends": [
        'website_blog',
    ],
    "data": [
        'views/templates.xml',
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
