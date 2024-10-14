#  Copyright 2024 Simone Rubino - Aion Tech
#  License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.tests import HttpCase


class TestIrHttp(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].sudo().get_current_website()
        self.auth_url = self.env["website.auth.url"].create(
            {"website_id": self.website.id, "path": "/contactus"}
        )
        self.user = self.env["res.users"].create(
            {"name": "Test User", "login": "test_user", "password": "12345"}
        )
        self.path = "/contactus"
        self.expected_path = "/web/login?redirect=%s" % self.path

    def test_dispatch_unauthorized(self):
        # Test that a public user cannot access "/auth_path
        self.authenticate(None, None)
        response = self.url_open(self.path, allow_redirects=False)
        self.assertEqual(
            response.status_code,
            302,
            "Expected the response status code to be 302 indicating a redirect",
        )

        self.assertIn(self.expected_path, response.headers["Location"])

    def test_dispatch_authorized(self):
        # Test that an authorized user can access "/auth_path
        self.authenticate(user="test_user", password="12345")
        response = self.url_open(self.path)
        self.assertEqual(
            response.status_code,
            200,
            "Expected the response status code to be 200 which means no redirection",
        )

    def test_authorize_everything(self):
        """Requiring "/" for authorization always redirects to login page."""
        # Arrange
        self.env["website.auth.url"].unlink()
        root_path = "/"
        self.env["website.auth.url"].create(
            {"website_id": self.website.id, "path": root_path}
        )
        self.env["ir.qweb"]._pregenerate_assets_bundles()
        asset_attachment = self.env["ir.attachment"].search(
            [
                ("url", "like", "/web/assets/%"),
            ],
            limit=1,
        )

        redirection_path_map = {
            "/": "/web/login?redirect=/",
            "/contactus": "/web/login?redirect=/contactus",
            asset_attachment.url: asset_attachment.url,
            "/web/login": "/web/login",
            "/jsonrpc": "/jsonrpc",
            "/xmlrpc/2/common": "/xmlrpc/2/common",
            "/xmlrpc/2/object": "/xmlrpc/2/object",
        }

        # Assert
        for requested_path, expected_redirected_path in redirection_path_map.items():
            response = self.url_open(requested_path)
            self.assertTrue(response.url.endswith(expected_redirected_path))
