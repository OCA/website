# Copyright 2024 Christopher Ormaza <chris.ormaza@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from urllib.parse import urlparse, urlunparse

from odoo import _, models


class Website(models.Model):
    _inherit = "website"

    def _get_dynamic_whatsapp_message(self, product=None):
        """
        Generate a dynamic WhatsApp message based on context.

        Args:
            product: product.template record or None

        Returns:
            str: The message text (not URL encoded)
        """
        if product and product.id:
            return (
                _("Hello, I'm interested in product %s, I would like more information")
                % product.display_name
            )
        return self.whatsapp_text or ""

    def _get_track_url_message(self, httprequest_full_path, product=None):
        """
        Override base method to support dynamic messages.

        Args:
            httprequest_full_path: The current page path
            product: product.template record or None

        Returns:
            str: Message with optional track URL (not URL encoded)
        """
        # Get dynamic or default message
        message = self._get_dynamic_whatsapp_message(product)

        # If track URL is enabled, append the formatted URL
        if self.whatsapp_track_url:
            sent_from = _("Sent from:")
            base_url = self.domain or self.env["ir.config_parameter"].sudo().get_param(
                "web.base.url"
            )
            url = f"{base_url}{httprequest_full_path}"
            parsed_url = urlparse(url)
            # Clean URL by removing query parameters
            cleaned_url = urlunparse(parsed_url._replace(query=""))
            # Append track URL with proper formatting
            return f"{message}%0A%0A*{sent_from} {cleaned_url}*"

        return message
