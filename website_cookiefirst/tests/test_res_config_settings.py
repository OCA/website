# Copyright 2023 NICO SOLUTIONS - ENGINEERNG & IT, Nils Coenen
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestResConfigSettings(TransactionCase):
    def setUp(self):
        super().setUp()
        self.res_config_settings = self.env["res.config.settings"]

    def test_cookiefirst_enabled(self):
        website = self.env["website"].create(
            {
                "name": "Test Website",
                "cookiefirst_identifier": "test_identifier",
            }
        )
        res_config_settings = self.res_config_settings.create(
            {
                "website_id": website.id,
                "cookiefirst_identifier": "test_identifier",
            }
        )
        self.assertTrue(res_config_settings.cookiefirst_enabled)
        res_config_settings.cookiefirst_enabled = False
        self.assertFalse(website.cookiefirst_identifier)
