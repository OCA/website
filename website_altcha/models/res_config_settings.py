# Copyright 2025 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import uuid

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    altcha_enabled = fields.Boolean(
        string="Enable Altcha",
        help="Enable Altcha functionality on the website.",
        compute="_compute_altcha_enabled",
        readonly=False,
    )
    altcha_key = fields.Char(
        related="website_id.altcha_key",
        readonly=False,
    )
    altcha_private_key = fields.Char(
        related="website_id.altcha_private_key",
        readonly=False,
    )
    altcha_algorithm = fields.Selection(
        related="website_id.altcha_algorithm",
        readonly=False,
    )
    altcha_timeout = fields.Integer(
        related="website_id.altcha_timeout",
        readonly=False,
    )
    altcha_cost = fields.Integer(
        related="website_id.altcha_cost",
        readonly=False,
    )

    @api.depends("altcha_key")
    def _compute_altcha_enabled(self):
        for record in self:
            record.altcha_enabled = bool(record.altcha_key)

    @api.onchange("altcha_enabled")
    def _onchange_altcha_enabled(self):
        for record in self:
            if not record.altcha_enabled:
                record.altcha_key = False
                record.altcha_private_key = False
            else:
                record.altcha_key = str(uuid.uuid4())
                record.altcha_private_key = str(uuid.uuid4())
