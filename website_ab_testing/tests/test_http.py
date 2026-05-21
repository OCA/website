from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install")
class TestHttp(HttpCase):
    def test_url_visited(self):
        self.homepage = self.env.ref("website.homepage")

        self.variant = self.env["ir.ui.view"].browse(
            self.homepage.create_variant("Variant 1")
        )
        self.env["ir.ui.view"].search([("key", "=", "website.homepage")]).write(
            {"arch": "<p>Goodbye</p>"}
        )
        self.logout()
        r = self.url_open("/")
        self.assertIn("Goodbye", r.text)
