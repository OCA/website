# Copyright 2023 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Snippet Dynamic Link",
    "category": "Website",
    "version": "15.0.1.0.0",
    "author": "Onestein, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "depends": [
        "website",
        "web_editor",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/website_dynamic_link_view.xml",
        "views/snippets/snippets.xml",
        "views/snippets/s_dynamic_link.xml",
        "menuitems.xml",
    ],
}
