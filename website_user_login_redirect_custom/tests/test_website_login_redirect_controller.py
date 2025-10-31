# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.tests import common, tagged

from odoo.addons.website_user_login_redirect_custom.controllers.main import (
    WebsiteRedirectCustom,
)


@tagged("post_install", "-at_install")
class TestWebsiteLoginRedirectController(common.TransactionCase):
    """Unit tests for WebsiteRedirectCustom controller"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteRedirectCustom()
        cls.config_parameter = cls.env["ir.config_parameter"].sudo()

        cls.portal_user = cls.env["res.users"].create(
            {
                "name": "Portal User",
                "login": "portal@test.com",
                "groups_id": [(4, cls.env.ref("base.group_portal").id)],
            }
        )

    def _fake_request(self, user, enabled=True, url="/shop"):
        """Create mock request for controller tests"""
        mock_req = MagicMock()
        mock_req.session.uid = user.id

        mock_user = MagicMock()
        mock_user.id = user.id
        if user.login.startswith("internal"):
            mock_user.has_group.side_effect = lambda g: g == "base.group_user"
        else:
            mock_user.has_group.side_effect = lambda g: g == "base.group_portal"

        mock_env = MagicMock()
        mock_env.user = mock_user

        def getitem(name):
            if name == "ir.config_parameter":
                ir_mock = MagicMock()
                ir_mock.sudo.return_value = ir_mock
                ir_mock.get_param.side_effect = lambda key, default=None: {
                    "website_user_login_redirect_custom.enabled": "True"
                    if enabled
                    else "False",
                    "website_user_login_redirect_custom.url": url,
                }.get(key, default)
                return ir_mock
            if name == "res.config.settings":
                settings_mock = MagicMock()
                settings_mock.is_valid_redirect_url.side_effect = (
                    lambda value: value
                    and value.startswith("/")
                    and not value.startswith("//")
                )
                return settings_mock
            raise KeyError(name)

        mock_env.__getitem__.side_effect = getitem
        mock_req.env = mock_env
        return mock_req

    def test_should_redirect_custom_portal_user_enabled(self):
        """Portal user with feature enabled should redirect"""
        mock_request = self._fake_request(self.portal_user, enabled=True)
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertTrue(self.controller._should_redirect_custom())

    def test_should_redirect_custom_internal_user(self):
        """Internal users should not redirect"""
        internal_user = self.env["res.users"].create(
            {
                "name": "Internal User",
                "login": "internal@test.com",
                "groups_id": [(4, self.env.ref("base.group_user").id)],
            }
        )
        mock_request = self._fake_request(internal_user, enabled=True)

        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            result = self.controller._should_redirect_custom()
            self.assertFalse(result)

    def test_get_custom_redirect_url(self):
        """Test custom URL validation and retrieval"""
        # Valid URL
        mock_request = self._fake_request(self.portal_user, url="/shop")
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertEqual(self.controller._get_custom_redirect_url(), "/shop")

        # Invalid URL
        mock_request = self._fake_request(self.portal_user, url="http://evil.com")
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertFalse(self.controller._get_custom_redirect_url())

    def test_should_redirect_custom_disabled(self):
        """Feature disabled → no redirect should occur"""
        mock_request = self._fake_request(self.portal_user, enabled=False)
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertFalse(self.controller._should_redirect_custom())

    def test_login_redirect_behavior(self):
        """Verify custom redirect applies when feature enabled"""
        mock_request = self._fake_request(
            self.portal_user, enabled=True, url="/thank-you"
        )
        with (
            patch(
                "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.controllers.home.Home._login_redirect",
                return_value="/my",
            ),
        ):
            result = self.controller._login_redirect(self.portal_user.id)
            self.assertEqual(result, "/thank-you")

    def test_should_redirect_custom_no_session(self):
        """Should not redirect if user session missing"""
        mock_request = MagicMock()
        mock_request.session.uid = None
        mock_request.env.user.has_group.return_value = False
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertFalse(self.controller._should_redirect_custom())

    def test_get_custom_redirect_url_empty(self):
        """Should return False if URL param is empty"""
        mock_request = MagicMock()
        mock_request.env[
            "ir.config_parameter"
        ].sudo.return_value.get_param.return_value = ""
        mock_request.env[
            "res.config.settings"
        ].is_valid_redirect_url.return_value = True
        with patch(
            "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
            mock_request,
        ):
            self.assertFalse(self.controller._get_custom_redirect_url())

    def test_login_redirect_returns_parent_redirect_when_disabled(self):
        """Return parent redirect when feature disabled"""
        mock_request = self._fake_request(self.portal_user, enabled=False, url="/shop")
        with (
            patch(
                "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.controllers.home.Home._login_redirect",
                return_value="/custom",
            ),
        ):
            result = self.controller._login_redirect(self.portal_user.id)
            self.assertEqual(result, "/custom")

    def test_login_redirect_applies_custom_url_on_my_path(self):
        """Custom redirect applies when parent_redirect is /my"""
        mock_request = self._fake_request(
            self.portal_user, enabled=True, url="/special"
        )
        with (
            patch(
                "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.controllers.home.Home._login_redirect",
                return_value="/my",
            ),
        ):
            result = self.controller._login_redirect(self.portal_user.id)
            self.assertEqual(result, "/special")

    def test_login_redirect_returns_parent_when_no_custom_url(self):
        """Return parent redirect if no valid custom URL found"""
        mock_request = self._fake_request(self.portal_user, enabled=True, url=None)
        with (
            patch(
                "odoo.addons.website_user_login_redirect_custom.controllers.main.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.controllers.home.Home._login_redirect",
                return_value="/my",
            ),
        ):
            result = self.controller._login_redirect(self.portal_user.id)
            self.assertEqual(result, "/my")
