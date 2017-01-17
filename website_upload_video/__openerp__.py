# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Upload video on website',
    'images': [],
    'category': 'Website',
    'version': '8.0.1.0.0',
    'author': 'ONESTEiN BV,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.onestein.eu',
    'depends': ['website'],
    'data': [
        'views/website_upload_video_views.xml'
    ],
    'qweb': [
        'static/src/xml/website_upload_video.xml'
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
