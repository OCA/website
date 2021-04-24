# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("website_id.cookiebot_id")
    def _compute_has_cookiebot_id(self):
        for record in self:
            record.update({"has_cookiebot_id": bool(record.cookiebot_id)})

    def _inverse_has_cookiebot_id(self):
        for record in self:
            if not record.has_cookiebot_id:
                record.website_id.update({"cookiebot_id": False})

    cookiebot_id = fields.Char(
        string="Cookiebot ID",
        related="website_id.cookiebot_id",
        readonly=False,
    )
    has_cookiebot_id = fields.Boolean(
        string="Use Cookiebot",
        compute="_compute_has_cookiebot_id",
        inverse="_inverse_has_cookiebot_id",
    )
