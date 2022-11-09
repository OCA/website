# Copyright 2022 Odoo S. A.
# Copyright 2022 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from werkzeug import urls

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    plausible_shared_key = fields.Char(
        "Plausible auth Key", related="website_id.plausible_shared_key", readonly=False
    )
    plausible_site = fields.Char(
        "Plausible Site (e.g. domain.com)",
        related="website_id.plausible_site",
        readonly=False,
    )
    has_plausible_shared_key = fields.Boolean(
        "Plausible Analytics",
        compute="_compute_has_plausible_shared_key",
        inverse="_inverse_has_plausible_shared_key",
    )

    @api.onchange("plausible_shared_key")
    def _onchange_shared_key(self):
        for config in self:
            value = config.plausible_shared_key
            if value and value.startswith("http"):
                try:
                    url = urls.url_parse(value)
                    config.plausible_shared_key = urls.url_decode(url.query).get(
                        "auth", ""
                    )
                    config.plausible_site = url.path.split("/")[-1]
                except Exception:  # noqa
                    pass

    @api.depends("website_id")
    def _compute_has_plausible_shared_key(self):
        for config in self:
            config.has_plausible_shared_key = bool(config.plausible_shared_key)

    def _inverse_has_plausible_shared_key(self):
        for config in self:
            if config.has_plausible_shared_key:
                continue
            config.plausible_shared_key = False
            config.plausible_site = False
