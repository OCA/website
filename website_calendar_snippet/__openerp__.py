# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Calendar Snippet',
    'images': [],
    'category': 'Website',
    'summary': 'Calendar (based on Messaging -> Calendar) on website.',
    'version': '8.0.1.0.0',
    'author': 'ONESTEiN BV,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': ['website', 'calendar', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'templates/website_calendar_snippet.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
