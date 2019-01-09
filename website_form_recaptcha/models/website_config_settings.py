# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    recaptcha_key_site = fields.Char(
        related='website_id.recaptcha_key_site',
    )
    recaptcha_key_secret = fields.Char(
        related='website_id.recaptcha_key_secret',
    )
