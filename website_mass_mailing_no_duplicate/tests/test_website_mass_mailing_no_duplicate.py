# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.http import request
from odoo.tests.common import TransactionCase, tagged

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_mass_mailing_no_duplicate.controllers.form import WebsiteForm


@tagged("post_install", "-at_install")
class TestWebsiteForm(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.mailing_list_1 = cls.env.ref("mass_mailing.mailing_list_1")
        cls.mailing_list_2 = cls.env.ref("mass_mailing.mailing_list_data")
        cls.mailingContact = cls.env["mailing.contact"]

    def _get_mailing_contact_qty(self):
        return len(self.mailingContact.with_context(active_test=False).search([]))

    def test_website_form_html_escaping(self):
        model = self.env["ir.model"].search([("model", "=", "mailing.contact")])

        original_qty = self._get_mailing_contact_qty()
        WebsiteFormController = WebsiteForm()

        vals = {
            "name": "/",
            "email": "BOB@BOB.com",
            "list_ids": [(6, 0, [self.mailing_list_1.id])],
        }

        with MockRequest(self.env, website=self.website):
            WebsiteFormController.insert_record(request, model, vals, "")
            self.assertEqual(
                self._get_mailing_contact_qty(),
                original_qty + 1,
                "subscribe should create a new mailing contact",
            )

            new_mailing_contact = self.mailingContact.search(
                [("email", "=", vals["email"])]
            )
            self.assertEqual(
                len(new_mailing_contact.list_ids),
                1,
                "subscribe to a mailing list should create an entry in list_ids",
            )

            vals["list_ids"] = [(6, 0, [self.mailing_list_2.id])]
            WebsiteFormController.insert_record(request, model, vals, "")
            self.assertEqual(
                self._get_mailing_contact_qty(),
                original_qty + 1,
                "subscribe to another mailing list should"
                " not create a new mailing contact",
            )
            self.assertEqual(
                len(new_mailing_contact.list_ids),
                2,
                "subscribe to another mailing list should"
                " create another entry in list_ids",
            )
