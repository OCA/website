# Copyright 2017 LasLabs Inc.
# Copyright 2020 Tecnativa - Alexandre Díaz
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase

from odoo.addons.website_legal_page.hooks import _merge_views


class TestController(HttpCase):
    def test_page(self):
        """It should return a 200 for legal page."""
        response = self.url_open("/legal", timeout=20)
        self.assertEqual(response.status_code, 200)

    def test_controller_redirection(self):
        """It should return a 200 for legal page.
        Can't run a specific test when 'website_sale' is installed because
        can't know if was be installed before or after 'website_legal_page'.

        If you install 'website_legal_page' after install 'website_sale' the
        module will be merge the 'website_sale.terms' view. But in the other
        direction this doesn't happens.
        """
        response = self.url_open("/terms", timeout=20)
        self.assertEqual(response.status_code, 200)
        module_id = self.env.ref("base.module_website_sale")
        if module_id.state != "installed":
            self.assertNotIn('href="#terms"', response.text)
        self.assertIn('id="section_list"', response.text)
        self.assertIn('id="section_content"', response.text)

    def test_hook(self):
        self.website_1 = self.env["website"].create({"name": "Website 1"})
        view_id = self.env["ir.ui.view"].create(
            {
                "arch": "<div id='wrap'><div>Test View</div></div>",
                "website_id": self.website_1.id,
                "key": "test.legal",
                "name": "Test Legal",
                "type": "qweb",
            }
        )
        self.env["website.page"].create(
            {
                "name": "Test Legal Page",
                "url": "/terms",
                "view_id": view_id.id,
                "is_published": True,
                "website_id": self.website_1.id,
                "website_indexed": True,
                "website_published": True,
            }
        )
        _merge_views(self.env, ["test.legal"])
        new_view_id = self.env["ir.ui.view"].search(
            [
                ("website_id", "=", self.website_1.id),
                ("key", "=", "website_legal_page.legal_page"),
            ]
        )
        self.assertTrue(new_view_id)
        self.assertIn("Test Legal Page", new_view_id.arch)
        self.assertIn("Test View", new_view_id.arch)
