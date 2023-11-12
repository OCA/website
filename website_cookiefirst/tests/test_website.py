# Copyright 2023 NICO SOLUTIONS - ENGINEERNG & IT, Nils Coenen
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestWebsite(TransactionCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].create(
            {"name": "Test Website", "cookiefirst_identifier": "1234567890"}
        )

    def test_cookiefirst_identifier(self):
        self.assertEqual(self.website.cookiefirst_identifier, "1234567890")
