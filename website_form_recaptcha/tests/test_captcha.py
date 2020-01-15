# Copyright 2015-2017 LasLabs Inc.
# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import mock

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase

imp_model = "odoo.addons.website_form_recaptcha.models.website_form_recaptcha"
imp_requests = "%s.requests" % imp_model


class TestCaptcha(TransactionCase):
    def setUp(self):
        super(TestCaptcha, self).setUp()
        self.model_obj = self.env["website.form.recaptcha"]
        self.validate_vars = "T1", "T2"
        self.website = self.env["website"].get_current_website()
        self.website.recaptcha_key_site = "test-site"
        self.website.recaptcha_key_secret = "test-secret"

    @mock.patch(imp_requests)
    def test_post_with_proper_data(self, mk):
        mk.post.side_effect = StopIteration
        exp1, exp2 = self.validate_vars
        try:
            self.model_obj._validate_response(exp1, exp2, website=self.website)
        except StopIteration:
            pass
        mk.post.assert_called_once_with(
            self.model_obj.URL,
            data={
                "secret": self.website.recaptcha_key_secret,
                "response": exp1,
                "remoteip": exp2,
            },
        )

    @mock.patch(imp_requests)
    def test_valid(self, mk):
        expect = {"success": True}
        mk.post().json.return_value = expect
        self.assertTrue(
            self.model_obj._validate_response(*self.validate_vars, website=self.website)
        )

    @mock.patch(imp_requests)
    def test_known_error_raises(self, mk):
        expect = {"error-codes": ["missing-input-secret"]}
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj._validate_response(*self.validate_vars, website=self.website)

    @mock.patch(imp_requests)
    def test_known_error_lookup(self, mk):
        expect = {"error-codes": ["missing-input-secret"]}
        mk.post().json.return_value = expect
        try:
            self.model_obj._validate_response(*self.validate_vars, website=self.website)
        except ValidationError as e:
            self.assertEqual(
                e.name, self.model_obj._get_error_message(expect["error-codes"][0])
            )

    @mock.patch(imp_requests)
    def test_unknown_error_lookup(self, mk):
        expect = {"error-codes": ["derp"]}
        mk.post().json.return_value = expect
        try:
            self.model_obj._validate_response(*self.validate_vars, website=self.website)
        except ValidationError as e:
            self.assertEqual(e.name, self.model_obj._get_error_message())

    @mock.patch(imp_requests)
    def test_no_success_raises(self, mk):
        expect = {"success": False}
        mk.post().json.return_value = expect
        with self.assertRaises(ValidationError):
            self.model_obj._validate_response(*self.validate_vars, website=self.website)

    def test_validate_request_no_value(self):
        request = object()
        req_values = {}
        with self.assertRaises(ValidationError) as err:
            self.model_obj._validate_request(request, req_values)
        self.assertEqual(err.exception.name, "The secret parameter is missing.")

    def test_validate_request_old_value(self):
        request = mock.MagicMock()
        request.g_recaptcha_response = "all good here"
        req_values = {}
        with mock.patch.object(type(self.model_obj), "_validate_response") as mocked:
            self.assertTrue(self.model_obj._validate_request(request, req_values))
            mocked.assert_not_called()

    def test_validate_request_validate_response(self):
        # Ensure that w/ proper conditions `validate_response is called`
        request = mock.MagicMock()
        request.g_recaptcha_response = None
        request.httprequest.environ = {}
        request.httprequest.remote_addr = "1.2.3.4"
        with mock.patch.object(type(self.model_obj), "_validate_response") as mocked:
            self.model_obj._validate_request(
                request, {self.model_obj.RESPONSE_ATTR: "validate_me"}
            )
            mocked.assert_called_with("validate_me", "1.2.3.4")
