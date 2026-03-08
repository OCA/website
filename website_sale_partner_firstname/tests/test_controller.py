from odoo.tests import tagged

from odoo.addons.website.tools import MockRequest
from odoo.addons.website_sale.tests.common import WebsiteSaleCommon
from odoo.addons.website_sale_partner_firstname.controllers.main import (
    WebsiteSaleFirstLastName,
)


@tagged('post_install', '-at_install')
class TestMandatoryFields(WebsiteSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteSaleFirstLastName()

    def test_get_mandatory_fields_removes_name(self):
        """Portal mandatory fields should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_fields()
        self.assertNotIn('name', fields)

    def test_get_mandatory_fields_has_firstname_lastname(self):
        """Portal mandatory fields should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_fields()
        self.assertIn('firstname', fields)
        self.assertIn('lastname', fields)

    def test_get_mandatory_address_fields_removes_name(self):
        """Checkout mandatory address fields should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_address_fields(
                self.country_us,
            )
        self.assertNotIn('name', fields)

    def test_get_mandatory_address_fields_has_firstname_lastname(self):
        """Checkout mandatory address fields should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            fields = self.controller._get_mandatory_address_fields(
                self.country_us,
            )
        self.assertIn('firstname', fields)
        self.assertIn('lastname', fields)


@tagged('post_install', '-at_install')
class TestDetailsFormValidate(WebsiteSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteSaleFirstLastName()

    def _base_data(self, **overrides):
        """Return a minimal valid form data dict for portal details."""
        data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'phone': '+1 555-555-5555',
            'email': 'john@example.com',
            'street': '123 Main St',
            'city': 'Springfield',
            'country_id': self.country_us.id,
            'zipcode': '62701',
        }
        data.update(overrides)
        return data

    def test_whitespace_firstname_triggers_error(self):
        """A whitespace-only firstname should be stripped and flagged missing."""
        data = self._base_data(firstname='   ')
        with MockRequest(self.env, website=self.website):
            error, error_message = self.controller.details_form_validate(data)
        self.assertEqual(error.get('firstname'), 'missing')

    def test_whitespace_lastname_triggers_error(self):
        """A whitespace-only lastname should be stripped and flagged missing."""
        data = self._base_data(lastname='   ')
        with MockRequest(self.env, website=self.website):
            error, error_message = self.controller.details_form_validate(data)
        self.assertEqual(error.get('lastname'), 'missing')

    def test_valid_names_pass_validation(self):
        """Normal firstname/lastname values should not produce errors."""
        data = self._base_data()
        with MockRequest(self.env, website=self.website):
            error, error_message = self.controller.details_form_validate(data)
        self.assertNotIn('firstname', error)
        self.assertNotIn('lastname', error)


@tagged('post_install', '-at_install')
class TestOnAccountUpdate(WebsiteSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteSaleFirstLastName()
        cls.test_partner = cls.env['res.partner'].create({
            'firstname': 'Jane',
            'lastname': 'Smith',
        })

    def test_name_injected_when_missing(self):
        """When 'name' is absent from values, it should be set from partner."""
        values = {'firstname': 'Jane', 'lastname': 'Smith'}
        with MockRequest(self.env, website=self.website):
            self.controller.on_account_update(values, self.test_partner)
        self.assertEqual(values['name'], self.test_partner.name)

    def test_name_not_overwritten_when_present(self):
        """When 'name' is already in values, it should not be changed."""
        values = {'name': 'Custom Name', 'firstname': 'Jane', 'lastname': 'Smith'}
        with MockRequest(self.env, website=self.website):
            self.controller.on_account_update(values, self.test_partner)
        self.assertEqual(values['name'], 'Custom Name')


@tagged('post_install', '-at_install')
class TestShopCountryInfo(WebsiteSaleCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.controller = WebsiteSaleFirstLastName()

    def test_required_fields_removes_name(self):
        """The required_fields list should not contain 'name'."""
        with MockRequest(self.env, website=self.website):
            result = self.controller.shop_country_info(
                self.country_us, 'billing',
            )
        self.assertNotIn('name', result['required_fields'])

    def test_required_fields_has_firstname_lastname(self):
        """The required_fields list should contain 'firstname' and 'lastname'."""
        with MockRequest(self.env, website=self.website):
            result = self.controller.shop_country_info(
                self.country_us, 'billing',
            )
        self.assertIn('firstname', result['required_fields'])
        self.assertIn('lastname', result['required_fields'])
