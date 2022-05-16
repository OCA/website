# Copyright 2022 Ooops (https://ooops404.com).
{
    "name": "Alter robots.txt disallow indexing based on server_environment",
    "summary": "Disables robots.txt for indexing by webcrawlers like Google,"
    "configuring in server_environment",
    "license": "LGPL-3",
    "version": "14.0.1.0.0",
    "website": "https://github.com/OCA/website",
    "author": "Ooops, Odoo Community Association (OCA)",
    "contributors": ["Ashish Hirpara"],
    "maintainers": ["AshishHirapara"],
    "category": "Website",
    "depends": [
        "website",
        "server_environment",
    ],
    "data": [
        "views/disable_robots.xml",
    ],
    "installable": True,
    "auto_install": True,
}
