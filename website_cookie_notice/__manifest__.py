# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Cookie notice",
    "summary": "Show cookie notice according to cookie law",
    "version": "13.0.1.0.0",
    "category": "Website",
    "author": "Agile Business Group, "
    "Tecnativa, "
    "Nicolas JEUDY, "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "depends": ["website_legal_page"],
    "data": ["views/assets.xml", "views/website.xml"],
    "post_init_hook": "post_init_hook",
}
