# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResGroups(models.Model):
    _inherit = 'res.groups'

    @api.model
    def get_page_groups(self, page):
        # Note now all pages have XMLID, but i verify again, in case some new
        # method of creating pages would make a non XMLID page.
        website = self.env['website'].search([], limit=1)
        # this if called via a website request will have website_id, and
        # therefore find the page. If I use it in the backend i need to inject
        # website_id in the context. Here I choose the only availiable website.
        # NOTE THIS FUNCTION WORKS ONLY FOR MONOWEBSITE PROJECTS
        self.with_context(website_id=website.id).env[
            'website'].check_page_xml_id(page)
        # now i am sure this will work.
        page_obj = self.env.ref(page)
        groups = self.search([()],)
        result = {}
        for group in groups:
            result[group.id] = [
                group.name, group in page_obj.page_permission_ids]
        return result
