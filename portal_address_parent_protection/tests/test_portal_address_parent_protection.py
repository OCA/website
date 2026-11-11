# Copyright 2026 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import patch

from odoo.http import Request
from odoo.tests import HttpCase, tagged
from odoo.tools import urls

from odoo.addons.base.tests.common import BaseCommon


@tagged("-at_install", "post_install")
class TestPortalAddressParentProtection(BaseCommon, HttpCase):
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
                "email": "company@example.com",
                "street": "Chau. de Namur 40",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": cls.country.id,
                "phone": "+3200000000000",
            }
        )
        cls.portal_user.partner_id.parent_id = cls.company_partner
        cls.submit_url = urls.urljoin(cls.base_url(), "/my/address/submit")

    # -- Edit rights -------------------------------------------------------

    def test_company_partner_not_editable_by_portal_user(self):
        company = self.company_partner.with_user(self.portal_user)
        self.assertFalse(company._can_be_edited_by_current_customer())
        own_address = self.portal_user.partner_id.with_user(self.portal_user)
        self.assertTrue(own_address._can_be_edited_by_current_customer())

    def test_sibling_address_still_editable_by_portal_user(self):
        sibling = self.env["res.partner"].create(
            {
                "name": "Warehouse",
                "type": "delivery",
                "parent_id": self.company_partner.id,
            }
        )
        self.assertTrue(
            sibling.with_user(self.portal_user)._can_be_edited_by_current_customer()
        )

    def test_child_company_not_editable_by_portal_user(self):
        subsidiary = self.env["res.partner"].create(
            {
                "name": "Subsidiary",
                "is_company": True,
                "type": "invoice",
                "parent_id": self.company_partner.id,
            }
        )
        self.assertFalse(
            subsidiary.with_user(self.portal_user)._can_be_edited_by_current_customer()
        )

    def test_company_not_editable_when_it_is_the_cart_customer(self):
        """``website_sale`` returns the cart customer from
        ``_get_current_partner()``, and ``website_sale_partner_sale_contact``
        sets that customer to the parent company. Core then considers the
        company to be the portal user's own record and grants full edit rights
        on it. The check must be anchored on the logged in user's partner."""
        company = self.company_partner.with_user(self.portal_user)
        with patch.object(
            type(self.env["res.partner"]),
            "_get_current_partner",
            lambda records, **kwargs: self.company_partner,
        ):
            # Core returns True here: ``self == current_partner``.
            self.assertFalse(company._can_be_edited_by_current_customer())

    # -- Company name ------------------------------------------------------

    def test_company_name_does_not_rename_parent(self):
        self.authenticate(self.portal_user.login, self.portal_user.login)
        self.url_open(
            self.submit_url,
            data={
                "csrf_token": Request.csrf_token(self),
                "partner_id": self.portal_user.partner_id.id,
                "name": "Portal Child",
                "email": "child@example.com",
                "street": "Rue de Ramillies 1",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": self.country.id,
                "phone": "+323333333333333",
                "company_name": "Renamed By Portal",
            },
        )
        # The request ran in another thread: do not assert on cached values.
        self.env.invalidate_all()
        self.assertEqual(self.company_partner.name, "Test Company SA")

    def test_company_name_on_a_new_address_does_not_rename_parent(self):
        """Exercise the creation path, where core does not drop
        ``company_name`` and ``_complete_address_values()`` makes the new
        address a child of the company.

        Core does not rename the parent there either, but only as a side effect
        of ``res.partner.create()`` blanking ``company_name`` in place on the
        values the rename block reads afterwards. This asserts the outcome the
        module guarantees regardless of that.
        """
        self.authenticate(self.portal_user.login, self.portal_user.login)
        self.url_open(
            self.submit_url,
            data={
                "csrf_token": Request.csrf_token(self),
                "address_type": "billing",
                "name": "New Billing Address",
                "email": "billing@example.com",
                "street": "Rue de la Facture 1",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": self.country.id,
                "phone": "+323333333333333",
                "company_name": "Renamed By Portal",
            },
        )
        self.env.invalidate_all()
        new_address = self.company_partner.child_ids.filtered(
            lambda partner: partner.name == "New Billing Address"
        )
        self.assertTrue(new_address, "the creation path was not exercised")
        self.assertEqual(self.company_partner.name, "Test Company SA")
        self.assertFalse(new_address.company_name)

    # -- Address synchronisation -------------------------------------------

    def test_own_address_change_does_not_move_company_address(self):
        """Core syncs a ``contact`` child's address up to its parent."""
        child = self.portal_user.partner_id
        self.assertEqual(child.street, self.company_partner.street)
        child.with_user(self.portal_user).sudo().write({"street": "Rue du Portail 1"})
        self.assertEqual(child.street, "Rue du Portail 1")
        self.assertEqual(self.company_partner.street, "Chau. de Namur 40")

    def test_own_address_submit_does_not_move_company_address(self):
        self.authenticate(self.portal_user.login, self.portal_user.login)
        self.url_open(
            self.submit_url,
            data={
                "csrf_token": Request.csrf_token(self),
                "partner_id": self.portal_user.partner_id.id,
                "name": "Portal Child",
                "email": "child@example.com",
                "street": "Rue du Portail 1",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": self.country.id,
                "phone": "+323333333333333",
            },
        )
        # The request ran in another thread: do not assert on cached values.
        self.env.invalidate_all()
        self.assertEqual(self.portal_user.partner_id.street, "Rue du Portail 1")
        self.assertEqual(self.company_partner.street, "Chau. de Namur 40")

    def test_internal_user_still_syncs_address_upstream(self):
        child = self.portal_user.partner_id
        child.write({"street": "Rue de l'Interne 1"})
        self.assertEqual(self.company_partner.street, "Rue de l'Interne 1")

    def test_attaching_a_contact_still_fills_the_company_address(self):
        """``website_sale_partner_sale_contact`` may create a company for a
        contact that typed a company name, and relies on core to copy the
        contact's address onto that new company."""
        new_company = self.env["res.partner"].create(
            {"name": "Brand New Co", "is_company": True}
        )
        contact = self.env["res.partner"].create(
            {
                "name": "Unattached Contact",
                "street": "Rue Neuve 1",
                "city": "Ramillies",
                "zip": "1367",
                "country_id": self.country.id,
            }
        )
        contact.with_user(self.portal_user).sudo().write({"parent_id": new_company.id})
        self.assertEqual(new_company.street, "Rue Neuve 1")
