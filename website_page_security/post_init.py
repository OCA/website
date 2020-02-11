# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, SUPERUSER_ID

def post_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    # give an XMLID to all previous pages
    pages = env['ir.ui.view'].search([('page', '=', True)])
    # NOTE THIS FUNCTION WORKS ONLY FOR MONOWEBSITE PROJECTS
    website = env['website'].search([], limit=1)
    for page in pages:
        env['website'].with_context(website_id=website.id).check_page_xml_id(
            template=page.key)
