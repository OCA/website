# Copyright 2026 Nitrokey GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_altcha.tests.common import Common


class TestWebsiteMassMailingAltcha(Common):
    def test_newsletter_subscription(self):
        """
        Test subscribing to a newsletter snippet
        """
        mailing_list = self.env.ref("website_mass_mailing_altcha.demo_mailing_list")
        self.start_tour(
            "/website_mass_mailing_altcha_demo", "website_mass_mailing_altcha"
        )
        self.assertIn(
            "test_website_mass_mailing_altcha@test.com",
            mailing_list.contact_ids.mapped("email"),
        )
