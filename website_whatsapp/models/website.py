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
