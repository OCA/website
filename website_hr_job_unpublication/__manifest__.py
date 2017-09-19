# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Website Hr Job Unpublication',
    'summary': """
        Allow employees to add a date to automatically
        unpublish a website jobs""",
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'ACSONE SA/NV,Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/website',
    'depends': [
        'hr',
        'website_hr_recruitment',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/hr_job.xml',
    ],
}
