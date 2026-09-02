# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_altcha.tests.common import Common


class TestWebsiteAltchaTours(Common):
    def test_contact_tour(self):
        """
        Run the contact test tour
        """
        self.start_tour("/contactus", "website_altcha_contact")

    def test_signup_tour(self):
        """
        Run the signup test tour
        """
        self.start_tour("/web/reset_password", "website_altcha_signup")

    def test_generic_tour(self):
        """
        Run the generic test tour
        """
        self.start_tour("/website_altcha_demo", "website_altcha_generic")
