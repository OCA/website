# Copyright 2025 - Escodoo, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0)

from odoo.tests.common import TransactionCase, tagged

from odoo.addons.website_google_analytics_4.controllers.website_sale import (
    WebsiteSaleInherit,
)


@tagged("post_install", "-at_install")
class TestWebsiteGoogleAnalytics4(TransactionCase):
    """Tests for the WebsiteSaleInherit controller in website_google_analytics_4 module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteSaleInherit()

        cls.categ = cls.env["product.category"].create({"name": "Test Category"})

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "barcode": "123456789",
                "categ_id": cls.categ.id,
                "list_price": 100.0,
            }
        )

        cls.sale_order = cls.env["sale.order"].create(
            {
                "partner_id": cls.env.ref("base.res_partner_1").id,
                "company_id": cls.env.ref("base.main_company").id,
                "currency_id": cls.env.ref("base.USD").id,
            }
        )

        cls.order_line = cls.env["sale.order.line"].create(
            {
                "order_id": cls.sale_order.id,
                "product_id": cls.product.id,
                "price_unit": 100.0,
                "product_uom_qty": 2,
            }
        )

    def test_order_lines_2_google_api(self):
        """Test order_lines_2_google_api returns correct data structure."""
        result = self.controller.order_lines_2_google_api([self.order_line])
        expected = [
            {
                "item_id": self.sale_order.id,
                "item_name": self.product.name,
                "sku": self.product.barcode,
                "item_category": self.categ.name,
                "price": self.order_line.price_unit,
                "quantity": self.order_line.product_uom_qty,
            }
        ]
        self.assertEqual(result, expected)

    def test_order_2_return_dict(self):
        """Test order_2_return_dict returns correctly formatted transaction dict."""
        # Set sale order amounts for testing
        self.sale_order.amount_total = 200.0
        self.sale_order.amount_tax = 20.0

        result = self.controller.order_2_return_dict(self.sale_order)
        expected = {
            "transaction": {
                "transaction_id": self.sale_order.id,
                "affiliation": self.sale_order.company_id.name,
                "value": self.sale_order.amount_total,
                "tax": self.sale_order.amount_tax,
                "currency": self.sale_order.currency_id.name,
                "items": [
                    {
                        "item_id": self.sale_order.id,
                        "item_name": self.product.name,
                        "sku": self.product.barcode,
                        "item_category": self.categ.name,
                        "price": self.order_line.price_unit,
                        "quantity": self.order_line.product_uom_qty,
                    }
                ],
            }
        }
        self.assertEqual(result, expected)
