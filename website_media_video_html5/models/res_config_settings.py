# Copyright 2026 Bosd
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    html5_video_allowed_hosts = fields.Char(
        string="Video Hosts",
        config_parameter="website_media_video_html5.allowed_hosts",
        help="Comma-separated list of hosts serving video files from URLs "
        "without a file extension, e.g. res.cloudinary.com. Subdomains are "
        "included.",
    )
