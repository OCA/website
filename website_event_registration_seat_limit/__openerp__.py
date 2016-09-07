# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# © 2016 Jamotion

{
    "name": "Seats per registration in website events",
    "version": "8.0.4.0.0",
    "category": "Tools",
    "author": "Jamotion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.jamotion.ch",
    "installable": True,
    "application": False,
    "summary": "Limit seats per registration",
    "depends": [
        "event_registration_seat_limit",
        "website_event_sale"
    ],
    "data": [
        "views/event_template.xml",
    ],
}
