from odoo.tests import tagged

from odoo.addons.website_sale.tests.common import MockRequest, WebsiteSaleCommon
from odoo.addons.website_sale_partner_firstname.controllers.main import (
    CustomerPortalFirstLastName,
)


@tagged("post_install", "-at_install")
class TestMandatoryFields(WebsiteSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = CustomerPortalFirstLastName()

    def test_billing_fields_removes_name(self):
        """Mandatory billing fields should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_billing_address_fields(
                self.country_us,
            )
        self.assertNotIn("name", fields)

    def test_billing_fields_has_firstname_lastname(self):
        """Mandatory billing fields should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_billing_address_fields(
                self.country_us,
            )
        self.assertIn("firstname", fields)
        self.assertIn("lastname", fields)

    def test_delivery_fields_removes_name(self):
        """Mandatory delivery fields should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_delivery_address_fields(
                self.country_us,
            )
        self.assertNotIn("name", fields)

    def test_delivery_fields_has_firstname_lastname(self):
        """Mandatory delivery fields should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_delivery_address_fields(
                self.country_us,
            )
        self.assertIn("firstname", fields)
        self.assertIn("lastname", fields)


@tagged("post_install", "-at_install")
class TestCountryInfo(WebsiteSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = CustomerPortalFirstLastName()

    def test_required_fields_removes_name(self):
        """The required_fields list should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            result = self.controller.portal_address_country_info(
                self.country_us,
                "billing",
            )
        self.assertNotIn("name", result["required_fields"])

    def test_required_fields_has_firstname_lastname(self):
        """The required_fields list should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            result = self.controller.portal_address_country_info(
                self.country_us,
                "billing",
            )
        self.assertIn("firstname", result["required_fields"])
        self.assertIn("lastname", result["required_fields"])


@tagged("post_install", "-at_install")
class TestCreateOrUpdateAddress(WebsiteSaleCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = CustomerPortalFirstLastName()

    def test_create_address_with_firstname_lastname(self):
        """Creating an address with firstname/lastname (no 'name') should work."""
        with MockRequest(self.env, website=self.website):
            partner, feedback = self.controller._create_or_update_address(
                self.env["res.partner"],  # empty recordset = create
                address_type="billing",
                verify_address_values=False,
                firstname="John",
                lastname="Doe",
                email="john@example.com",
                street="123 Main St",
                city="Springfield",
                country_id=str(self.country_us.id),
                phone="555-1234",
            )
        self.assertTrue(partner.exists())
        self.assertEqual(partner.firstname, "John")
        self.assertEqual(partner.lastname, "Doe")

    def test_update_address_with_firstname_lastname(self):
        """Updating an existing address with firstname/lastname should not KeyError."""
        partner = self.env["res.partner"].create(
            {
                "firstname": "Jane",
                "lastname": "Smith",
                "email": "jane@example.com",
                "street": "456 Oak Ave",
                "city": "Shelbyville",
                "country_id": self.country_us.id,
            }
        )
        with MockRequest(self.env, website=self.website):
            updated_partner, feedback = self.controller._create_or_update_address(
                partner.sudo(),
                address_type="billing",
                verify_address_values=False,
                firstname="Janet",
                lastname="Smith",
                email="jane@example.com",
                street="456 Oak Ave",
                city="Shelbyville",
                country_id=str(self.country_us.id),
                phone="555-5678",
            )
        self.assertEqual(updated_partner.firstname, "Janet")
        self.assertEqual(updated_partner.lastname, "Smith")


@tagged("post_install", "-at_install")
class TestFrontendWritableFields(WebsiteSaleCommon):
    def test_firstname_lastname_writable(self):
        """'firstname' and 'lastname' should be in frontend writable fields."""
        writable = self.env["res.partner"]._get_frontend_writable_fields()
        self.assertIn("firstname", writable)
        self.assertIn("lastname", writable)
