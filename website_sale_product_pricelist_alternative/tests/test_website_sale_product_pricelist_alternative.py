# Copyright 2024 Camptocamp (<https://www.camptocamp.com>).
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.product_pricelist_alternative.tests.common import (
    CommonProductPricelistAlternative,
)


class TestWebsiteSaleProductPricelistAlternative(CommonProductPricelistAlternative):
    def test_get_combination_info(self):
        # Setup website.
        website = self.env["website"].create(
            {
                "name": "Test website",
                "company_id": self.env.company.id,
                "user_id": self.env.user.id,
                "pricelist_ids": [Command.set(self.pricelist01.ids)],
            }
        )
        # Without discount policy.
        self.pricelist01.discount_policy = "without_discount"
        datacard = self.datacard.product_tmpl_id.with_context(website_id=website.id)
        combination_info = datacard._get_combination_info(pricelist=self.pricelist01)
        self.assertEqual(combination_info["list_price"], 70.0)
        self.assertEqual(combination_info["price"], 70.0)
        self.assertFalse(combination_info["has_discounted_price"])
        res = datacard._get_sales_prices(pricelist=self.pricelist01)
        self.assertEqual(res[datacard.id]["base_price"], 70.0)
        self.assertEqual(res[datacard.id]["price_reduce"], 70.0)

        usb_adapter = self.usb_adapter.product_tmpl_id.with_context(
            website_id=website.id
        )
        combination_info = usb_adapter._get_combination_info(pricelist=self.pricelist01)
        self.assertEqual(combination_info["list_price"], 95.0)
        self.assertEqual(combination_info["price"], 70.0)
        self.assertTrue(combination_info["has_discounted_price"])
        res = usb_adapter._get_sales_prices(pricelist=self.pricelist01)
        self.assertEqual(res[usb_adapter.id]["base_price"], 95.0)
        self.assertEqual(res[usb_adapter.id]["price_reduce"], 70.0)
