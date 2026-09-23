from odoo.tests.common import TransactionCase

from odoo.addons.http_routing.tests.common import MockRequest
from odoo.addons.website_field_autocomplete.controllers.main import Website


class TestWebsiteFieldAutocomplete(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.current_website = cls.env["website"].get_current_website()

    def test_get_field_autocomplete(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Website Field Autocomplete Test Partner",
                "parent_id": self.current_website.user_id.partner_id.id,
            }
        )
        payload = {
            "domain": [["id", "=", partner.id]],
            "fields": ["name"],
            "limit": 5,
        }
        with MockRequest(self.env, website=self.current_website):
            response = Website()._get_field_autocomplete(model="res.partner", **payload)

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["name"], partner.name)

    def test_get_field_autocomplete_rejects_missing_fields(self):
        payload = {
            "domain": [],
            "fields": [],
        }
        with MockRequest(self.env, website=self.current_website):
            response = Website()._get_field_autocomplete(model="res.partner", **payload)

        self.assertEqual(response, [])
