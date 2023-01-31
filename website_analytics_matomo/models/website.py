# Copyright 2015 Therp BV <http://therp.nl>
# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from urllib.parse import urlparse

from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    has_matomo_analytics = fields.Boolean("Matomo Analytics")
    matomo_analytics_id = fields.Char(
        "Matomo website ID",
        help="The ID Matomo uses to identify the website",
        default="1",
    )
    matomo_analytics_host = fields.Char(
        "Matomo host",
        help="The host/path your Matomo installation is "
        "accessible by on the internet.",
    )
    matomo_analytics_host_url = fields.Char(
        string="Matomo host URL",
        compute="_compute_matomo_analytics_host_url",
        store=True,
    )
    matomo_enable_heartbeat = fields.Boolean()
    matomo_heartbeat_timer = fields.Integer(
        help="How many seconds a tab needs to be active to be counted as viewed.",
        default=15,
    )
    matomo_enable_userid = fields.Boolean()
    matomo_get_userid = fields.Char(compute="_compute_matomo_userid")

    @api.depends("matomo_analytics_host")
    def _compute_matomo_analytics_host_url(self):
        """Formats a proper Matomo host URL based on matomo_analytics_host"""
        for website in self.filtered(lambda w: not w.matomo_analytics_host):
            website.matomo_analytics_host_url = ""
        for website in self.filtered(lambda w: w.matomo_analytics_host):
            parsed_url = urlparse(website.matomo_analytics_host)
            if parsed_url.scheme not in ("http", "https"):
                parsed_url = parsed_url._replace(scheme="https")
            host_url = parsed_url.geturl()
            host_url = host_url.rstrip("/")  # Remove potential trailing slash
            website.matomo_analytics_host_url = host_url

    @api.depends_context("uid")
    @api.depends("matomo_analytics_host", "matomo_enable_userid")
    def _compute_matomo_userid(self):
        """Gets the unique user ID of the current user. Here we assume that user ID
        is the "login" field of "res.users".
        Override this method if you want to use a different user ID.
        """
        for website in self.filtered(
            lambda w: not w.matomo_analytics_host or not w.matomo_enable_userid
        ):
            website.matomo_get_userid = ""
        for website in self.filtered(
            lambda w: w.matomo_analytics_host and w.matomo_enable_userid
        ):
            if self.env.user != website.user_id:  # current user is logged in
                website.matomo_get_userid = str(self.env.user.id)
            else:
                website.matomo_get_userid = ""
