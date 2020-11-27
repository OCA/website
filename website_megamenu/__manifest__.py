# Copyright 2020 Odoo
# Copyright 2020 Tecnativa - Alexandre Díaz
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Website Megamenu",
    "category": "Menu/Megamenu",
    "summary": "Adds support for mega menus",
    "version": "12.0.1.1.0",
    "license": "LGPL-3",
    "depends": ["website"],
    "data": ["templates/assets.xml", "templates/website.xml", "templates/snippets.xml"],
    "qweb": ["static/src/xml/website.contentMenu.xml"],
    "author": "Odoo S.A., Tecnativa, Odoo Community Association (OCA)",
    "installable": True,
    "maintainers": ["Tardo"],
}
