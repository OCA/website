# Copyright 2022 Studio73 - Ioan Galan <ioan@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    @api.depends("website_id.sendinblue_identifier")
    def _compute_sendinblue_enabled(self):
        for record in self:
            record.update({"sendinblue_enabled": bool(record.sendinblue_identifier)})

    def _inverse_sendinblue_enabled(self):
        for record in self:
            if not record.sendinblue_enabled:
                record.website_id.update({"sendinblue_identifier": False})

    sendinblue_identifier = fields.Char(
        string="Sendinblue ID",
        related="website_id.sendinblue_identifier",
        readonly=False,
    )
    sendinblue_enabled = fields.Boolean(
        string="Use Sendinblue",
        compute="_compute_sendinblue_enabled",
        inverse="_inverse_sendinblue_enabled",
    )
