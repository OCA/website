# Copyright 2022 Studio73 - Ioan Galan <ioan@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("website_id.whatsapp_number")
    def _compute_whatsapp_enabled(self):
        for record in self:
            record.update({"whatsapp_enabled": bool(record.whatsapp_number)})

    def _inverse_whatsapp_enabled(self):
        for record in self:
            if not record.whatsapp_enabled:
                record.website_id.update({"whatsapp_number": False})

    whatsapp_number = fields.Char(
        related="website_id.whatsapp_number",
        readonly=False,
    )
    whatsapp_text = fields.Char(
        related="website_id.whatsapp_text",
        readonly=False,
    )
    whatsapp_track_url = fields.Boolean(
        related="website_id.whatsapp_track_url",
        readonly=False,
    )
    whatsapp_enabled = fields.Boolean(
        string="Use Whatsapp",
        compute="_compute_whatsapp_enabled",
        inverse="_inverse_whatsapp_enabled",
    )
