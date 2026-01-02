# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import request
from odoo.tools import str2bool

from odoo.addons.web.controllers.home import Home


class WebsiteRedirectCustom(Home):
    """
    Inherit from Home to override login redirect behavior
    Using _login_redirect hook like portal module does
    """

    def _should_redirect_custom(self):
        """Check if we should perform custom redirect"""
        if not request.session.uid:
            return False

        # Do not redirect backend/internal users
        if request.env.user.has_group("base.group_user"):
            return False

        enabled = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website_user_login_redirect_custom.enabled", "False")
        )
        return str2bool(enabled)

    def _get_custom_redirect_url(self):
        """Get custom redirect URL or False if not set/valid"""
        url = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website_user_login_redirect_custom.url", "/")
        )
        if not url:
            return False
        url = url.strip()
        if request.env["res.config.settings"].is_valid_redirect_url(url):
            return url

        return False

    def _login_redirect(self, uid, redirect=None):
        """
        Override login redirect behavior for portal users
        Redirect to custom URL instead of /my when feature is enabled
        """
        # First call parent to get default redirect (e.g., portal users to /my)
        parent_redirect = super()._login_redirect(uid, redirect=redirect)

        # Apply our custom redirect logic
        if self._should_redirect_custom():
            # Only apply custom redirect for cases where user would go to /my
            # or when there's no specific redirect
            if not parent_redirect or "/my" in parent_redirect:
                custom_url = self._get_custom_redirect_url()
                if custom_url:
                    return custom_url

        return parent_redirect
