from datetime import datetime

from freezegun import freeze_time

from odoo.addons.event.tests.test_event_internals import TestEventInternalsCommon


class testWebsiteEventNoRegistration(TestEventInternalsCommon):
    @freeze_time("2020-1-31 10:00:00")
    def test_event_registrable(self):
        """Test if `_compute_event_registrations_open` works properly."""
        self.event_0.write(
            {
                "date_begin": datetime(2020, 1, 30, 8, 0, 0),
                "date_end": datetime(2020, 1, 31, 8, 0, 0),
            }
        )
        self.assertFalse(self.event_0.event_registrations_open)
        self.event_0.write(
            {
                "date_end": datetime(2020, 2, 4, 8, 0, 0),
            }
        )
        self.assertTrue(self.event_0.event_registrations_open)

        self.event_0.write({"registration_allowed": False})
        self.assertFalse(self.event_0.event_registrations_open)
