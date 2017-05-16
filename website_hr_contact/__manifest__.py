# -*- coding: utf-8 -*-
# © 2015-2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Hr Contact",
    'summary': """
        Display your hr address book in your website
    """,
    'author': 'ACSONE SA/NV,'
              'Odoo Community Association (OCA)',
    'website': "http://acsone.eu",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'website_hr',
    ],

    'data': [
        'views/website_hr_contact_templates.xml',
        'data/website_hr_contact_data.xml',
    ],
}
