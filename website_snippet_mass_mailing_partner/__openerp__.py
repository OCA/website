# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Mass Mailing Subscription Snippet With Name",
    "summary": "Ask for name when subscribing, and create and/or link partner",
    "version": "8.0.1.0.0",
    "category": "Website",
    "website": "https://tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "mass_mailing_partner",
    ],
    "data": [
        "views/assets.xml",
        "views/snippets.xml",
    ],
}
