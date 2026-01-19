# Copyright 2016 ABF OSIELL <http://osiell.com>
# Copyright 2018 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import re

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    google_tag_manager_key = fields.Char("Container ID")

    def _clean_gtm_key(self, gtm_key):
        """Clean GTM key by removing extra quotes and whitespace"""
        if not gtm_key:
            return ""
        # Remove extra quotes (both single and double)
        cleaned = re.sub(r'^["\']+|["\']+$', "", gtm_key.strip())
        # Remove any remaining quotes in the middle
        cleaned = cleaned.replace('"', "").replace("'", "")
        return cleaned.strip()

    def get_gtm_key(self):
        """Get cleaned GTM key for use in templates"""
        if not self.google_tag_manager_key:
            return ""
        return self._clean_gtm_key(self.google_tag_manager_key)

    @api.model_create_multi
    def create(self, vals_list):
        """Clean GTM key before creating"""
        for vals in vals_list:
            if "google_tag_manager_key" in vals:
                vals["google_tag_manager_key"] = self._clean_gtm_key(
                    vals.get("google_tag_manager_key", "")
                )
        return super().create(vals_list)

    def write(self, vals):
        """Clean GTM key before writing"""
        if "google_tag_manager_key" in vals:
            vals["google_tag_manager_key"] = self._clean_gtm_key(
                vals.get("google_tag_manager_key", "")
            )
        return super().write(vals)
