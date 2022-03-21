#  Copyright 2022 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from ..controllers.main import PortalAddress
from odoo.tests import SavepointCase

CONTACT_MODULE_PATH = 'odoo.addons.website_portal_contact'


class TestPortalAddress (SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = PortalAddress()

    def test_contacts_clean_values_state(self):
        """
        Check that even if fake, country and state fields are not cleaned out.
        """
        values = {
            'country_id': 'fake_country_id',
            'state_id': 'fake_country_id-fake_state_id',
        }

        contact_request_path = '%s.controllers.main.request' \
                               % CONTACT_MODULE_PATH
        with patch(contact_request_path) as contact_request:
            contact_request.env = self.env
            clean_values = self.controller._contacts_clean_values(values)

        self.assertTrue(values.items() <= clean_values.items())
