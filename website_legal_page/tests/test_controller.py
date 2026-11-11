# Copyright 2017 LasLabs Inc.
# Copyright 2020 Tecnativa - Alexandre Díaz
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestController(HttpCase):
    def test_page(self):
        """It should return a 200 for legal page."""
        response = self.url_open("/legal", timeout=20)
        self.assertEqual(response.status_code, 200)
