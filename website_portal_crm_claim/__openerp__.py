# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
{
    "name": "Claims in Website Portal",
    "summary": "Follow your claims directly in your website portal",
    "version": "9.0.1.0.0",
    "category": "Website",
    "website": "https://www.tecnativa.com/",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "crm_claim",
        "website_crm_claim",  # FIXME See known issues; drop in v10
        "website_portal_v10",
    ],
    "data": [
        "data/mail_alias_data.xml",
        "templates/crm_claim.xml",
        "templates/layout.xml",
        "templates/website_portal.xml",
        "wizards/sale_config_settings_view.xml",
    ],
    "demo": [
        "demo/assets_demo.xml",
    ],
}
