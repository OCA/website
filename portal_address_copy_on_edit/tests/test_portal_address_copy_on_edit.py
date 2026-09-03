# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import Request
from odoo.tests import HttpCase, tagged
from odoo.tools import urls

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestPortalAddressCopyOnEdit(BaseCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.quick_ref("base.be")
        cls.env.company.country_id = cls.country
        cls.portal_user = cls._create_new_portal_user(login="portal_child")
        cls.company_partner = cls.env["res.partner"].create(
            {
                "name": "Test Company SA",
                "is_company": True,
                "street": "Chau. de Namur 40",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": cls.country.id,
            }
        )
        cls.portal_user.partner_id.parent_id = cls.company_partner
        cls.delivery_address = cls.env["res.partner"].create(
            {
                "name": "Warehouse",
                "type": "delivery",
                "parent_id": cls.company_partner.id,
                "street": "Rue du Depot 1",
                "email": "address@example.com",
                "phone": "+3200000000000",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": cls.country.id,
            }
        )
        cls.submit_url = urls.urljoin(cls.base_url(), "/my/address/submit")

    def _submit(self, partner, street, address_type="delivery", name=None):
        self.authenticate(self.portal_user.login, self.portal_user.login)
        self.url_open(
            self.submit_url,
            data={
                "csrf_token": Request.csrf_token(self),
                "partner_id": partner.id,
                "address_type": address_type,
                "name": name or partner.name,
                "street": street,
                "email": "address@example.com",
                "phone": "+3200000000000",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": self.country.id,
            },
        )
        # The request ran in another thread: do not assert on cached values.
        self.env.invalidate_all()

    def test_edited_address_is_copied(self):
        """Editing an address leaves the original untouched."""
        self._submit(self.delivery_address, "Rue Neuve 2")
        self.assertEqual(
            self.delivery_address.street,
            "Rue du Depot 1",
            "the edited address must keep the value its documents were issued with",
        )
        copies = self.company_partner.child_ids.filtered(
            lambda partner: partner.street == "Rue Neuve 2"
        )
        self.assertEqual(len(copies), 1, "a new address must have been created")
        self.assertNotEqual(copies, self.delivery_address)
        self.assertEqual(copies.type, "delivery", "the new address keeps the type")
        self.assertEqual(copies.parent_id, self.company_partner)

    def test_original_address_is_not_archived(self):
        """The address the documents point at stays visible."""
        self._submit(self.delivery_address, "Rue Neuve 2")
        self.assertTrue(self.delivery_address.active)

    def test_editing_twice_copies_twice(self):
        """Each edit is a new address, however recent the previous one is."""
        self._submit(self.delivery_address, "Rue Neuve 2")
        copy = self.company_partner.child_ids.filtered(
            lambda partner: partner.street == "Rue Neuve 2"
        )
        self._submit(copy, "Rue Neuve 3")
        self.assertEqual(copy.street, "Rue Neuve 2")
        self.assertTrue(
            self.company_partner.child_ids.filtered(
                lambda partner: partner.street == "Rue Neuve 3"
            )
        )

    def test_unchanged_values_never_create_a_copy(self):
        """Opening the form and saving it unchanged must not duplicate."""
        children_before = self.company_partner.child_ids
        self._submit(self.delivery_address, self.delivery_address.street)
        self.assertEqual(self.company_partner.child_ids, children_before)

    def test_own_contact_record_is_always_edited_in_place(self):
        """The customer's own record is their own data, never a copy."""
        own = self.portal_user.partner_id
        children_before = self.company_partner.child_ids
        self._submit(own, "Rue Personnelle 3", address_type="billing")
        self.assertEqual(own.street, "Rue Personnelle 3")
        self.assertEqual(self.company_partner.child_ids, children_before)
