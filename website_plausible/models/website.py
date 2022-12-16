# Copyright 2022 Odoo S. A.
# Copyright 2022 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from werkzeug import urls

from odoo import fields, models


class Website(models.Model):
    _inherit = "website"

    plausible_shared_key = fields.Char()
    plausible_site = fields.Char()

    def _get_plausible_script_url(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(
                "website.plausible_script", "https://plausible.io/js/plausible.js"
            )
        )

    def _get_plausible_server(self):
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("website.plausible_server", "https://plausible.io")
        )

    def _get_plausible_share_url(self):
        embed_url = (
            f"/share/{self.plausible_site}"
            f"?auth={self.plausible_shared_key}&embed=true&theme=system"
        )
        return (
            self.plausible_shared_key
            and urls.url_join(self._get_plausible_server(), embed_url)
            or ""
        )
