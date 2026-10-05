# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Website Event - No registration",
    "summary": "Add option to prevent registration of event"
    " organized by third party.",
    "version": "18.0.1.0.0",
    "author": "GRAP, Odoo Community Association (OCA)",
    "maintainers": ["legalsylvain"],
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "category": "Website",
    "depends": ["website_event"],
    "data": [
        "views/view_event_event.xml",
        "views/event_templates.xml",
        "views/view_event_type.xml",
    ],
}
