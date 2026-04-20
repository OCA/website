# Copyright 2026 Binhex <https://www.binhex.cloud>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    sitemap_excluded_paths = fields.Text(
        related="website_id.sitemap_excluded_paths",
        readonly=False,
    )

    def action_reload_sitemap(self):
        self.ensure_one()
        website = self.website_id or self.env["website"].get_current_website()
        website._clear_sitemap_cache()
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Sitemap reloaded"),
                "message": _(
                    "The cached sitemap has been cleared for the current website."
                ),
                "type": "success",
                "sticky": False,
            },
        }
