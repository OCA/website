from odoo.tests.common import TransactionCase

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_field_autocomplete.controllers.main import (
    Website,  # Asumiendo que esta es tu clase extendida
)


class TestWensiteFieldAutocomplete(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.current_website = cls.env["website"].get_current_website()

    def test_get_field_autocomplete(self):
        Partner = self.env["res.partner"]
        Partner.create({"name": "Test Partner"})
        payload = {
            "domain": [["name", "ilike", "Test"]],
            "fields": ["name"],
            "limit": 5,
        }
        with MockRequest(self.env, website=self.current_website):
            response = Website()._get_field_autocomplete(model="res.partner", **payload)
            self.assertIsInstance(response, list, "Debe devolver una lista")
            self.assertTrue(len(response) > 0, "Debe encontrar al menos un registro")
            self.assertEqual(response[0]["name"], "Test Partner")
