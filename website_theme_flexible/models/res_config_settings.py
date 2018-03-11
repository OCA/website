# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_font_api_key = fields.Char(
        name='Google Fonts API Key',
        related='website_id.google_font_api_key'
    )
