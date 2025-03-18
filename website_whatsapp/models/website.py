# Copyright 2022 Studio73 - Ioan Galan <ioan@studio73.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from urllib.parse import urlparse, urlunparse

from odoo import _, fields, models


class Website(models.Model):
    _inherit = "website"

    whatsapp_number = fields.Char(string="WhatsApp number")
    whatsapp_text = fields.Char(
        "Default text for Whatsapp",
        help="Default text to send as message",
        translate=True,
    )
    whatsapp_track_url = fields.Boolean(
        "Track URL",
        help="Indicate in the user's message the URL of the page from which it "
        "was sent",
    )
    whatsapp_included_country_ids = fields.Many2many(
        string="Show Whatsapp only in Countries",
        comodel_name="res.country",
        relation="website_whatsapp_included_countries_rel",
        help="When set, the whatsapp icon will only appear to the selected countries.",
    )
    whatsapp_excluded_country_ids = fields.Many2many(
        string="Do not show Whatsapp in Countries",
        comodel_name="res.country",
        relation="website_whatsapp_excluded_countries_rel",
        help="When set, the whatsapp icon will only appear when the "
        "country of the user is not within this list.",
    )

    def _get_track_url_message(self, httprequest_full_path):
        sent_from = _("Sent from:")
        base_url = self.domain or self.env["ir.config_parameter"].sudo().get_param(
            "web.base.url"
        )
        url = f"{base_url} {httprequest_full_path}"
        parsed_url = urlparse(url)
        cleaned_url = urlunparse(parsed_url._replace(query=""))
        if self.whatsapp_track_url:
            whatsapp_track_url_text = (
                f"{self.whatsapp_text} %0A%0A*{sent_from} {cleaned_url}*"
            )
        return whatsapp_track_url_text

    def _check_display_whatsapp_icon(self, request):
        self.ensure_one()
        if not self.whatsapp_number:
            return False
        geoip_country_code = request.geoip.get("country_code")
        country = request.env["res.country"].sudo()
        if geoip_country_code:
            country = (
                request.env["res.country"]
                .sudo()
                .search([("code", "=", geoip_country_code)], limit=1)
            )
        if (
            country
            and self.whatsapp_included_country_ids
            and country not in self.whatsapp_included_country_ids
        ):
            return False
        if (
            country
            and self.whatsapp_excluded_country_ids
            and country in self.whatsapp_excluded_country_ids
        ):
            return False
        return True
