# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    recaptcha_key_site = fields.Char(
        related="website_id.recaptcha_key_site", readonly=False
    )
    recaptcha_key_secret = fields.Char(
        related="website_id.recaptcha_key_secret", readonly=False
    )
    has_google_recaptcha = fields.Boolean(
        "Google reCaptcha",
        compute="_compute_has_google_recaptcha",
        inverse="_inverse_has_google_recaptcha",
        readonly=False,
    )

    @api.depends("website_id")
    def _compute_has_google_recaptcha(self):
        for config in self:
            config.has_google_recaptcha = bool(config.recaptcha_key_site)

    def _inverse_has_google_recaptcha(self):
        for config in self:
            if not config.has_google_recaptcha:
                config.recaptcha_key_site = False
                config.recaptcha_key_secret = False
