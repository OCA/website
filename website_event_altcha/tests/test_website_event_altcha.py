# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.website_altcha.tests.common import Common


class TestWebsiteEventAltcha(Common):
    def test_event_registration_with_questions(self):
        """
        Test an event registration that contains questions
        """
        event = self.env.ref("event.event_7")
        self.start_tour(f"/event/{event.id}", "website_event_altcha")
