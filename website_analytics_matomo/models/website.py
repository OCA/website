# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    has_matomo_analytics = fields.Boolean("Matomo Analytics")
    matomo_analytics_id = fields.Char(
        "Matomo website ID",
        help="The ID Matomo uses to identify the website",
        default=1,
    )
    matomo_analytics_host = fields.Char(
        "Matomo host",
        help="The host/path your Matomo installation is "
        "accessible by on the internet. Do not include a protocol here!\n"
        "So http[s]://[this field]/matomo.php should resolve to your matomo.php",
    )
