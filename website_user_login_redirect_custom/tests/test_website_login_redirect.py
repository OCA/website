# Copyright (C) 2025 Cetmix OÜ
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestWebsiteLoginRedirect(common.TransactionCase):
    """Test website login redirect functionality"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config_parameter = cls.env["ir.config_parameter"].sudo()

        # Create test users once for all tests
        cls.internal_user = cls.env["res.users"].create(
            {
                "name": "Internal User",
                "login": "internal@test.com",
                "groups_id": [(4, cls.env.ref("base.group_user").id)],
            }
        )
        cls.portal_user = cls.env["res.users"].create(
            {
                "name": "Portal User",
                "login": "portal@test.com",
                "groups_id": [(4, cls.env.ref("base.group_portal").id)],
            }
        )

    def test_enable_redirect_feature(self):
        """Test enabling redirect feature through settings"""
        settings = self.env["res.config.settings"].create({})
        settings.website_login_redirect_enabled = True
        settings.website_login_redirect_url = "/shop"
        settings.execute()

        self.assertEqual(
            self.config_parameter.get_param(
                "website_user_login_redirect_custom.enabled"
            ),
            "True",
        )
        self.assertEqual(
            self.config_parameter.get_param("website_user_login_redirect_custom.url"),
            "/shop",
        )

    def test_url_validation_accepts_valid_urls(self):
        """Test that URL validation accepts valid relative URLs"""
        settings = self.env["res.config.settings"].create({})
        valid_urls = ["/", "/shop", "/web#home", "/my/custom/path", "/page?param=value"]
        for url in valid_urls:
            self.assertTrue(settings.is_valid_redirect_url(url))

    def test_url_validation_rejects_invalid_urls(self):
        """Test that URL validation rejects invalid URLs"""
        settings = self.env["res.config.settings"].create({})
        invalid_urls = [
            "shop",
            "http://evil.com",
            "https://test.com",
            "//phish.com",
            "javascript:alert(1)",
            "data:text/html;base64,xxx",
            "vbscript:msgbox(1)",
        ]
        for url in invalid_urls:
            with self.subTest(url=url):
                with self.assertRaises(ValidationError) as cm:
                    settings.website_login_redirect_url = url
                    settings._check_url_format()

                # Verify it's the specific error message we expect
                self.assertIn(
                    "Custom URL must be a valid relative path starting with '/'",
                    str(cm.exception),
                )

    def test_empty_url_validation(self):
        """Test validation with empty URL when enabled"""
        settings = self.env["res.config.settings"].create({})
        settings.website_login_redirect_enabled = True

        # Should allow empty URL (will use default)
        settings.website_login_redirect_url = False
        settings._check_url_format()  # Should not raise

        # Should allow None
        settings.website_login_redirect_url = None
        settings._check_url_format()  # Should not raise

    def test_onchange_normalizes_whitespace(self):
        settings = self.env["res.config.settings"].create({})
        settings.website_login_redirect_url = "  /shop  "
        settings._onchange_website_login_redirect_url()
        self.assertEqual(settings.website_login_redirect_url, "/shop")

    def test_is_valid_redirect_url_edge_cases(self):
        """Test URL validation with edge cases"""
        settings = self.env["res.config.settings"].create({})

        # Test double slash rejection
        self.assertFalse(settings.is_valid_redirect_url("//evil.com"))

        # Test single slash acceptance
        self.assertTrue(settings.is_valid_redirect_url("/"))

        # Test whitespace handling
        self.assertTrue(settings.is_valid_redirect_url(" /shop "))

        # Test None input
        self.assertFalse(settings.is_valid_redirect_url(None))

        # Test empty string
        self.assertFalse(settings.is_valid_redirect_url(""))

    def test_check_url_format_skips_empty(self):
        """_check_url_format should skip empty URLs"""
        settings = self.env["res.config.settings"].create({})
        settings._check_url_format()  # Should not raise

    def test_is_valid_redirect_url_rejects_external(self):
        """Reject external URLs with scheme or domain"""
        settings = self.env["res.config.settings"].create({})
        self.assertFalse(settings.is_valid_redirect_url("http://evil.com"))

    def test_check_url_format_raises_validation_error(self):
        """Invalid URL triggers ValidationError during create"""
        with self.assertRaises(ValidationError):
            self.env["res.config.settings"].create(
                {"website_login_redirect_url": "javascript:alert(1)"}
            )

    def test_onchange_strips_url_whitespace(self):
        """Onchange removes leading/trailing spaces in URL"""
        settings = self.env["res.config.settings"].create(
            {"website_login_redirect_url": "   /clean-me   "}
        )
        settings._onchange_website_login_redirect_url()
        self.assertEqual(settings.website_login_redirect_url, "/clean-me")
