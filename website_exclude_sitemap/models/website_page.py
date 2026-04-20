# Copyright 2026 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    _SITEMAP_CACHE_FIELDS = {
        "url",
    }

    def _get_sitemap_cache_websites(self):
        website_id = self.website_id
        if any(not page.website_id for page in self):
            website_id |= self.env["website"].search([])
        return website_id

    @api.model_create_multi
    def create(self, vals_list):
        pages = super().create(vals_list)
        pages._get_sitemap_cache_websites()._clear_sitemap_cache()
        return pages

    def write(self, vals):
        websites = self._get_sitemap_cache_websites()
        result = super().write(vals)
        if self._SITEMAP_CACHE_FIELDS.intersection(vals):
            (websites | self._get_sitemap_cache_websites())._clear_sitemap_cache()
        return result

    def unlink(self):
        websites = self._get_sitemap_cache_websites()
        result = super().unlink()
        websites._clear_sitemap_cache()
        return result
