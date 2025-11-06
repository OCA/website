# Copyright 2025 - Today: GRAP https://www.grap.coop
# License AGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    social_mastodon = fields.Char(
        "Mastodon Account", default=lambda x: x._default_social_mastodon()
    )

    def _default_social_mastodon(self):
        return self.env.company.social_mastodon

    def read(self, fields=None, load="_classic_read"):
        # the list of social media loaded in the front office
        # is hard coded in the function '_fetchSocialMedia'.
        # (website/static/src/snippets/s_social_media/options.js)
        if all([x.startswith("social_") for x in fields]):
            fields.append("social_mastodon")
        return super().read(fields=fields, load=load)
