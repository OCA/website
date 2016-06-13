# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Fair Data for Events",
    "summary": "New fields needed to work with fairs",
    "version": "8.0.1.1.0",
    "category": "Event Management",
    "website": "http://www.antiun.com",
    "author": "Antiun Ingeniería S.L., Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale_extra_info",
        "website_event_track",
    ],
    "data": [
        "views/event_registration_view.xml",
    ],
}
