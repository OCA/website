# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cookiebot_id = fields.Char(
        "Cookiebot ID", related="website_id.cookiebot_id", readonly=False,
    )
