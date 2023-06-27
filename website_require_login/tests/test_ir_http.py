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
