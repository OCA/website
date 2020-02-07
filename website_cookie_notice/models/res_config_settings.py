# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cookie_notice_legal_page_id = fields.Many2one(
        related="website_id.cookie_notice_legal_page_id", readonly=False
    )
