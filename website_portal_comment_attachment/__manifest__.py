# Copyright 2019 ABF OSIELL <http://osiell.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Website Portal Comment Attachment",
    "summary": "Add an attachment on any portal comments",
    "version": "12.0.1.0.0",
    "category": "Website",
    "website": "http://github.com/OCA/website",
    "author": "Osiell, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "portal",
    ],
    "data": [
        "views/assets.xml",
    ],
    'qweb': [
        'static/src/xml/portal_chatter.xml',
    ]
}
