# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class WebsiteConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    multi_theme_id = fields.Many2one(related="website_id.multi_theme_id")

    def multi_theme_reload(self):
        """Update multiwebsite themes when loading a new wizard."""
        _logger.info("Reloading available multi-website themes")
        # Reload available single-website converted themes
        self.env["website.theme"].search([])._convert_assets()
        # Reload custom views for themes activated in any website
        self.env["website"].search([])._multi_theme_activate()
