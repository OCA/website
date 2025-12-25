# Copyright 2025 Quartile (https://www.quartile.co)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from types import SimpleNamespace
from unittest.mock import patch

from odoo.tests.common import TransactionCase

from odoo.addons.website_form_partner_specific_user_account.controllers.main import (
    WebsiteForm,
)


class TestWebsiteFormSimple(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company_1 = cls.env["res.company"].create({"name": "Company 1"})
        cls.company_2 = cls.env["res.company"].create({"name": "Company 2"})
        cls.website_1 = cls.env["website"].create(
            {
                "name": "Website 1",
                "specific_user_account": True,
                "restrict_partner_to_company": True,
                "company_id": cls.company_1.id,
            }
        )
        cls.website_2 = cls.env["website"].create(
            {
                "name": "Website 2",
                "specific_user_account": True,
                "restrict_partner_to_company": False,
                "company_id": cls.company_2.id,
            }
        )

    def mock_insert_record(self, request, model, values, custom, meta=None):
        return values

    def _req(self, website):
        return SimpleNamespace(env=self.env, website=website)

    @patch(
        "odoo.addons.website.controllers.form.WebsiteForm.insert_record",
        new=mock_insert_record,
    )
    def test_partner_website_and_company_when_restricted(self):
        partner = self.env["res.partner"].create(
            {
                "name": "Partner",
                "email": "test1@example.com",
                "company_id": False,
            }
        )
        WebsiteForm().insert_record(
            self._req(self.website_1),
            "res.partner",
            {
                "partner_id": partner.id,
                "email_from": partner.email,
            },
            {},
        )
        self.assertEqual(partner.website_id, self.website_1)
        self.assertEqual(partner.company_id, self.company_1)

    @patch(
        "odoo.addons.website.controllers.form.WebsiteForm.insert_record",
        new=mock_insert_record,
    )
    def test_website_partner_with_existing_website(self):
        original = self.env["res.partner"].create(
            {
                "name": "Original",
                "email": "test2@example.com",
                "website_id": self.website_1.id,
                "company_id": False,
            }
        )
        WebsiteForm().insert_record(
            self._req(self.website_2),
            "res.partner",
            {
                "partner_id": original.id,
                "email_from": original.email,
                "partner_name": "Website 2 Partner",
            },
            {},
        )
        website_partner = self.env["res.partner"].search(
            [
                ("email", "=", original.email),
                ("website_id", "=", self.website_2.id),
            ],
            limit=1,
        )
        self.assertTrue(website_partner)
        self.assertNotEqual(website_partner, original)
        # Compare against website_2's company instead of using assertFalse,
        # because another module may assign a default company.
        # In this test environment, the current company is base.main_company.
        self.assertNotEqual(website_partner.company_id, self.website_2.company_id)

    @patch(
        "odoo.addons.website.controllers.form.WebsiteForm.insert_record",
        new=mock_insert_record,
    )
    def test_website_partner_with_company_when_restricted(self):
        self.website_2.restrict_partner_to_company = True
        original = self.env["res.partner"].create(
            {
                "name": "Original",
                "email": "test3@example.com",
                "website_id": self.website_1.id,
                "company_id": False,
            }
        )
        original.company_id = False
        WebsiteForm().insert_record(
            self._req(self.website_2),
            "res.partner",
            {
                "partner_id": original.id,
                "email_from": original.email,
                "partner_name": "Restricted Partner",
            },
            {},
        )
        website_partner = self.env["res.partner"].search(
            [
                ("email", "=", original.email),
                ("website_id", "=", self.website_2.id),
                ("company_id", "=", self.website_2.company_id.id),
            ],
            limit=1,
        )
        self.assertTrue(website_partner)
