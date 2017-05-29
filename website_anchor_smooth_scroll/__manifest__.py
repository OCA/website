# -*- coding: utf-8 -*-
# Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Smooth Scroll for Website Anchors',
    'summary': 'Replace default behavior for internal links (anchor only) with'
               ' smooth scroll',
    'version': '10.0.1.0.0',
    'category': 'Website',
    'website': 'http://www.antiun.com',
    'author': 'Antiun Ingeniería S.L., '
              'Tecnativa, '
              'LasLabs, '
              'Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website',
    ],
    'data': [
        'views/website_anchor_smooth_scroll.xml',
    ],
    'demo': [
        'demo/website_anchor_smooth_scroll.xml',
    ],
}
