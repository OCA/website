# Copyright 2019 Tecnativa - Sergio Teruel
# Copyright 2019 Tecnativa - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    'name': 'Website Event Filter Organizer',
    'summary': 'Filter events by organizer in frontend',
    'version': '12.0.1.0.0',
    'category': "website",
    'author': 'Tecnativa, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'depends': ['website_event'],
    'data': [
        'views/website_event.xml',
    ],
    'installable': True,
}
