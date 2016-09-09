# -*- coding: utf-8 -*-
# © 2013-2016 Odoo S.A.
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Payment: Website Integration (Adapted to Backport From v10)',
    'category': 'Website',
    'summary': 'Payment: Website Integration',
    'version': '9.0.1.0.0',
    'author': 'Odoo S.A.,'
              'Tecnativa,'
              'Odoo Community Association (OCA)',
    'depends': [
        'website_payment',
        'website_portal_v10',
    ],
    'data': [
        'views/website_payment_templates.xml',
    ],
    'auto_install': True,
}
