# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': "Departments Page",
    'summary': """
        Display the structure of your departments and their members.
        """,
    'author': "ACSONE SA/NV,Odoo Community Association (OCA)",
    'website': "http://acsone.eu",
    'category': 'Website',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'website_hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/website_hr_department_security.xml',
        'data/websiste_hr_department_data.xml',
        'views/website_hr_department.xml',
    ],
    'installable': True,
}
