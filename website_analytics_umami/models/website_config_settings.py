# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    has_umami_analytics = fields.Boolean(
        "Umami Analytics", related="website_id.has_umami_analytics", readonly=False
    )
    umami_analytics_id = fields.Char(
        related="website_id.umami_analytics_id", readonly=False
    )
    umami_analytics_host = fields.Char(
        related="website_id.umami_analytics_host", readonly=False
    )
    # umami_script_name = fields.Char(
    #     related="website_id.umami_script_name", readonly=False
    # )
