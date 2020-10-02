# Copyright 2020 Commown SCIC SAS (https://commown.fr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
from odoo.addons.website_sale_promotion_rule.controllers.main import WebsiteSale
from odoo.addons.website.tools import MockRequest


class TestWebsitePromotionRule(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestWebsitePromotionRule, cls).setUpClass()
        cls.website = cls.env.ref("website.website2")
        cls.website_sale = cls.env.ref("website_sale.website_sale_order_1")
        data_coupon = {
            "name": "Best Promo",
            "code": "ELDONGHUT",
            "rule_type": "coupon",
            "usage_restriction": "no_restriction",
            "promo_type": "discount",
            "discount_amount": 20.00,
            "discount_type": "percentage",
            "minimal_amount": 0.00,
            "is_minimal_amount_tax_incl": False,
            "multi_rule_strategy": "exclusive",
        }
        cls.promotion_rule_coupon = cls.env["sale.promotion.rule"].create(
            data_coupon)
        cls.website_sale.write({"website_id": cls.website.id})
        cls.WebsiteSaleController = WebsiteSale()

    def test_apply_promotion_rule(self):
        self.assertEqual(self.website_sale.coupon_promotion_rule_id.id, False)
        self.assertEqual(self.website_sale.amount_total, 599.00)
        with MockRequest(self.env, website=self.website,
                         sale_order_id=self.website_sale.id):
            self.WebsiteSaleController.pricelist(
                self.promotion_rule_coupon.code)
            self.assertEqual(self.website_sale.coupon_promotion_rule_id.code,
                             "ELDONGHUT")
        self.assertEqual(self.website_sale.amount_total, 479.20)
