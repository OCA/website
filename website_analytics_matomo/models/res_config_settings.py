# Copyright 2015 Therp BV <http://therp.nl>
# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    has_matomo_analytics = fields.Boolean(
        "Matomo Analytics",
        related="website_id.has_matomo_analytics",
        readonly=False,
    )
    matomo_analytics_id = fields.Char(
        related="website_id.matomo_analytics_id", readonly=False
    )
    matomo_analytics_host = fields.Char(
        related="website_id.matomo_analytics_host", readonly=False
    )
    matomo_enable_heartbeat = fields.Boolean(
        related="website_id.matomo_enable_heartbeat", readonly=False
    )
    matomo_heartbeat_timer = fields.Integer(
        related="website_id.matomo_heartbeat_timer", readonly=False
    )
    matomo_enable_userid = fields.Boolean(
        related="website_id.matomo_enable_userid", readonly=False
    )
