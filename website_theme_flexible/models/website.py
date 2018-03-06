# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    theme_flexible_id = fields.Many2one(
        comodel_name='theme.flexible'
    )

    google_font_api_key = fields.Char(
        name='Google Fonts API Key'
    )
