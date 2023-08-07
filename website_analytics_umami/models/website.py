# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    has_umami_analytics = fields.Boolean("Umami Analytics")
    umami_analytics_id = fields.Char(
        "Umami Website ID", help="The unique Umami ID uses to identify the website"
    )
    umami_analytics_host = fields.Char(
        "Umami Host",
        help="The host/path your Umami instance is "
        "accessible by on the internet. Do not include a protocol here!\n"
        "So http[s]://[this field]/script.js should resolve to your umami.js",
    )
    # umami_script_name = fields.Char(
    #     "Script Name",
    #     help="The name of the script to load. Defaults to umami.js"
    #     " You can leave it as is unless you have a custom script",
    #     default="umami.js",
    # )

    def _get_umami_script_url(self):
        self.ensure_one()
        return f"https://{self.umami_analytics_host}/script.js"
