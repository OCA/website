# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from openerp import api, models
from openerp.http import request


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def enumerate_pages(self, query_string=None):
        """Show redirected URLs in search results."""
        query = query_string or ""
        seo_redirections = list()
        redirection_records = self.env["website.seo.redirection"].search([
            "|", ("origin", "ilike", query),
            ("destination", "ilike", query),
        ])
        for record in redirection_records:
            for url in record.origin, record.destination:
                if url not in seo_redirections:
                    seo_redirections.append(url)
        # Give super() a website to work with
        if not request.website_enabled:
            self.ensure_one()
            request.website = self
        # Yield super()'s pages
        for page in super(Website, self).enumerate_pages(query_string):
            try:
                seo_redirections.remove(page["loc"])
            except ValueError:
                pass
            yield page
        # Remove website if we were supposed to have none
        if not request.website_enabled:
            request.website = None
        # Yield redirected pages not detected by super()
        for page in seo_redirections:
            yield {"loc": page}
