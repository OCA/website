# -*- coding: utf-8 -*-
# © 2013-2016 Odoo S.A.
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Payment: Website Integration (Backported From v10)',
    'category': 'Website',
    'summary': 'Payment: Website Integration',
    'version': '9.0.1.0.0',
    'depends': [
        'website',
        'payment',
        'website_portal_v10',
    ],
    'data': [
        'views/website_payment_view.xml',
        'views/website_payment_templates.xml',
        'views/res_config_view.xml',
    ],
    'auto_install': False,
}
