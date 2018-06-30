# -*- coding: utf-8 -*-
# © 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Snippet Breadcrumb",
    'summary': """Website Snippet Breadcrumb""",
    'author': "Acsone SA/NV, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    'website': "http://www.acsone.eu",
    'category': 'Website',
    'version': '8.0.1.0.0',
    'depends': [
        'website_breadcrumb',
        'website_node_branded',
    ],
    'data': [
        'views/assets.xml',
        'views/snippets.xml',
    ],
}
