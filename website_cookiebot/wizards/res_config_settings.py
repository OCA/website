# Copyright 2020 Trey - Antonio González <antonio@trey.es>
# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cookiebot_dgid = fields.Char(
        string="Domain Group ID",
        related="website_id.cookiebot_dgid",
        readonly=False,
    )
    cookiebot_enabled = fields.Boolean(
        string="Cookiebot",
        compute="_compute_cookiebot_enabled",
        readonly=False,
    )

    @api.depends("website_id.cookiebot_dgid")
    def _compute_cookiebot_enabled(self):
        for record in self:
            record.cookiebot_enabled = bool(record.cookiebot_dgid)
