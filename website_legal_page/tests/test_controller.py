# Copyright 2017 LasLabs Inc.
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase
from odoo.tools import mute_logger


class TestController(HttpCase):
    def _test_page(self, page, code=200):
        response = self.url_open(page, timeout=20)
        self.assertEqual(response.status_code, code)

    @mute_logger("odoo.addons.website.models.ir_ui_view")
    def test_unknown(self):
        """ It should return a 404 for unknown pages. """
        self._test_page('/legal/no-page', 404)

    def test_privacy(self):
        """ It should return a 200 for privacy policy page. """
        self._test_page('/legal/privacy-policy')

    def test_advice(self):
        """ It should return a 200 for advice page. """
        self._test_page('/legal/advice')

    def test_tos(self):
        """ It should return a 200 for ToS page. """
        self._test_page('/legal/terms-of-use')
