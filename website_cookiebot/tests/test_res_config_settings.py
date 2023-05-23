# Copyright 2021 NICO SOLUTIONS - ENGINEERING & IT, Nils Coenen
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResConfigSettings(TransactionCase):
    def setUp(self):
        super(TestResConfigSettings, self).setUp()
        self.website = self.env["website"].create(
            {"name": "Test Website", "cookiebot_dgid": "test_dgid"}
        )
        self.res_config_settings = self.env["res.config.settings"].create(
            {"website_id": self.website.id}
        )

    def test_compute_cookiebot_enabled(self):
        self.res_config_settings._compute_cookiebot_enabled()
        self.assertTrue(self.res_config_settings.cookiebot_enabled)

    def test_compute_cookiebot_enabled_no_dgid(self):
        self.website.cookiebot_dgid = False
        self.res_config_settings._compute_cookiebot_enabled()
        self.assertFalse(self.res_config_settings.cookiebot_enabled)
