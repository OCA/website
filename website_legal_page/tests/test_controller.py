# Copyright 2017 LasLabs Inc.
# Copyright 2020 Tecnativa - Alexandre Díaz
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestController(HttpCase):
    def test_page(self):
        """ It should return a 200 for legal page. """
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
        response = self.url_open("/shop/terms", timeout=20)
        self.assertEqual(response.status_code, 200)
        module_id = self.env.ref("base.module_website_sale")
        if module_id.state != "installed":
            self.assertNotIn('href="#terms"', response.text)
        self.assertIn('id="section_list"', response.text)
        self.assertIn('id="section_content"', response.text)
