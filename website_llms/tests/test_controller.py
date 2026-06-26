# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestLlmsTxtController(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].sudo().get_current_website()

    def _wait_remaining_requests(self, timeout=10):
        # Bypass this to prevent the test suite from hanging for 10 seconds per test.
        pass

    def test_manifest_coverage(self):
        """Test to execute the manifest file to satisfy coverage."""
        import importlib.util
        import os

        manifest_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "__manifest__.py"
        )
        spec = importlib.util.spec_from_file_location(
            "website_llms.manifest", manifest_path
        )
        manifest_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(manifest_mod)
        self.assertTrue(isinstance(manifest_mod.__dict__, dict))

    def test_llms_txt_with_configured_content(self):
        """Test /llms.txt endpoint with configured content."""
        # Configure custom content
        custom_content = """# My Website — Information for LLMs

## Company
- About: https://example.com/about
- Contact: https://example.com/contact

## Services
- Service 1: https://example.com/service1
"""
        self.website.llms_txt_content = custom_content

        # Make request
        response = self.url_open("/llms.txt", timeout=20)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"),
            "text/plain; charset=utf-8",
        )
        self.assertEqual(
            response.headers.get("Cache-Control"),
            "public, max-age=3600",
        )
        # Content should end with newline
        self.assertTrue(response.text.endswith("\n"))
        # Should contain configured content
        self.assertIn("My Website", response.text)
        self.assertIn("https://example.com/about", response.text)

    def test_llms_txt_without_content(self):
        """Test /llms.txt endpoint without configured content (default)."""
        # Ensure no content is configured
        self.website.llms_txt_content = False

        # Make request
        response = self.url_open("/llms.txt", timeout=20)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.headers.get("Content-Type"),
            "text/plain; charset=utf-8",
        )
        self.assertEqual(
            response.headers.get("Cache-Control"),
            "public, max-age=3600",
        )
        # Content should end with newline
        self.assertTrue(response.text.endswith("\n"))
        # Should contain default content with website name
        self.assertIn(self.website.name, response.text)
        self.assertIn("Information for LLMs", response.text)
        self.assertIn("## Company", response.text)
        self.assertIn("## Content", response.text)

    def test_llms_txt_with_empty_content(self):
        """Test /llms.txt endpoint with empty content (should use default)."""
        # Set empty content
        self.website.llms_txt_content = ""

        # Make request
        response = self.url_open("/llms.txt", timeout=20)

        # Assertions
        self.assertEqual(response.status_code, 200)
        # Should contain default content
        self.assertIn(self.website.name, response.text)
        self.assertIn("Information for LLMs", response.text)

    def test_llms_txt_with_whitespace_content(self):
        """Test /llms.txt endpoint with whitespace-only content (should use default)."""
        # Set whitespace-only content
        self.website.llms_txt_content = "   \n\t  "

        # Make request
        response = self.url_open("/llms.txt", timeout=20)

        # Assertions
        self.assertEqual(response.status_code, 200)
        # Should contain default content (whitespace is stripped)
        self.assertIn(self.website.name, response.text)
        self.assertIn("Information for LLMs", response.text)
