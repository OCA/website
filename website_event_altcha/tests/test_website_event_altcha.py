# Copyright 2026 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import Command, fields

from odoo.addons.website_altcha.tests.common import Common


class TestWebsiteEventAltcha(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        now = fields.Datetime.now()
        cls.event = cls.env["event.event"].create(
            {
                "name": "Altcha Test Event",
                "date_tz": "Europe/Brussels",
                "date_begin": now - timedelta(days=1),
                "date_end": now + timedelta(days=1),
                "is_published": True,
                "question_ids": [
                    Command.create(
                        {
                            "title": "Name",
                            "question_type": "name",
                            "is_mandatory_answer": True,
                        }
                    ),
                    Command.create(
                        {
                            "title": "Email",
                            "question_type": "email",
                            "is_mandatory_answer": True,
                        }
                    ),
                    Command.create(
                        {
                            "title": "Phone",
                            "question_type": "phone",
                        }
                    ),
                ],
            }
        )

    def test_event_registration_with_questions(self):
        """
        Test an event registration that contains questions
        """
        self.start_tour(f"/event/{self.event.id}", "website_event_altcha")
