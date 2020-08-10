# Copyright 2020 Radovan Skolnik <radovan@skolnik.info>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


{
    "name": "Website Menu Icons",
    "category": "Website",
    "license": "AGPL-3",
    "author": "Radovan Skolnik, Odoo Community Association (OCA)",
    "version": "13.0.1.0.0",
    "summary": """
Provides possibility to define icons/images for menus.
These can be then rendered in a custom theme.
It also brings back option for opening new window.
    """,
    "depends": ["website"],
    "data": ["views/assets.xml", "views/website_menu_icon.xml"],
    "installable": True,
}
