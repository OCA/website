# Copyright 2026 MTS - Juan Arcos
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestWebsiteSaleVatLabel(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country_custom = cls.env["res.country"].search([], limit=1)
        cls.country_custom.vat_label = "RUT"

        cls.country_default = cls.env["res.country"].create(
            {
                "name": "Test Country No Label",
                "code": "XX",
                "vat_label": False,
            }
        )

    def test_prepare_address_form_values_via_controller(self):
        """Test country-specific VAT labels through the website sale controller."""
        self.authenticate("admin", "admin")

        response_custom = self.url_open(
            f"/shop/address?country_id={self.country_custom.id}"
        )
        self.assertEqual(response_custom.status_code, 200)

        response_default = self.url_open(
            f"/shop/address?country_id={self.country_default.id}"
        )
        self.assertEqual(response_default.status_code, 200)
