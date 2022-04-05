# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl)

from odoo import fields, models


class PortalConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    recaptcha_key_site = fields.Char(
        config_parameter="portal_recaptcha.recaptcha_key_site"
    )
    recaptcha_key_secret = fields.Char(
        config_parameter="portal_recaptcha.recaptcha_key_secret"
    )
