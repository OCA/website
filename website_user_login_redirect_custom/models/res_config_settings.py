# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from urllib.parse import urlparse

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    website_login_redirect_enabled = fields.Boolean(
        string="On Login/Signup Redirect",
        config_parameter="website_user_login_redirect_custom.enabled",
        help="If checked, users will be redirected to a custom URL after login/signup.",
    )

    website_login_redirect_url = fields.Char(
        string="Custom URL",
        config_parameter="website_user_login_redirect_custom.url",
        help="Relative URL path where users will be redirected after login/signup. "
        "Example: '/', '/shop', '/thank-you-for-joining-us'.",
    )

    @staticmethod
    def is_valid_redirect_url(url) -> bool:
        """Validate that URL is a safe relative path for redirects"""
        if not url:
            return False

        url = url.strip()

        # Must start with single '/', not '//' and not contain schemes
        if not (url == "/" or (url.startswith("/") and not url.startswith("//"))):
            return False

        # Parse and ensure no scheme or netloc
        parsed = urlparse(url)
        if parsed.scheme or parsed.netloc:
            return False

        return True

    @api.constrains("website_login_redirect_url")
    def _check_url_format(self):
        """Ensure URL is a valid relative path."""
        for rec in self:
            url = (rec.website_login_redirect_url or "").strip()

            if not url:
                continue

            if not self.is_valid_redirect_url(url):
                raise ValidationError(
                    _("Custom URL must be a valid relative path starting with '/'.")
                )

    @api.onchange("website_login_redirect_url")
    def _onchange_website_login_redirect_url(self):
        """Normalize whitespace in the URL."""
        if self.website_login_redirect_url:
            stripped = self.website_login_redirect_url.strip()
            if stripped != self.website_login_redirect_url:
                self.website_login_redirect_url = stripped
