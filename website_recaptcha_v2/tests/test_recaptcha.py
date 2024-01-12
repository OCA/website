# SPDX-FileCopyrightText: 2022 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from unittest import mock

from odoo.tests.common import TransactionCase

imp_requests = "odoo.addons.website_recaptcha_v2.models.website.requests"


class TestRecaptcha(TransactionCase):
    def setUp(self):
        super().setUp()
        self.website = self.env.ref("website.default_website")
        self.website.write(
            {
                "recaptcha_enabled": True,
                "recaptcha_key_site": "test-site",
                "recaptcha_key_secret": "test-secret",
            }
        )

    @mock.patch(imp_requests)
    def test_captcha_http_request(self, requests_mock):
        requests_mock.post.side_effect = StopIteration
        try:
            self.website.is_captcha_valid({"g-recaptcha-response": "dummy_response"})
        except StopIteration:
            pass
        requests_mock.post.assert_called_once_with(
            "https://www.recaptcha.net/recaptcha/api/siteverify",
            data={
                "secret": "test-secret",
                "response": "dummy_response",
            },
        )

    @mock.patch(imp_requests)
    def test_captcha_valid(self, requests_mock):
        requests_mock.post().json.return_value = {"success": True}
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertTrue(result)
        self.assertEqual(error_msg, "")

    @mock.patch(imp_requests)
    def test_captcha_single_error(self, requests_mock):
        requests_mock.post().json.return_value = {
            "error-codes": ["missing-input-secret"]
        }
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertFalse(result)
        self.assertEqual(error_msg, "The secret parameter is missing.")

    @mock.patch(imp_requests)
    def test_captcha_multiple_errors(self, requests_mock):
        requests_mock.post().json.return_value = {
            "error-codes": ["invalid-input-secret", "missing-input-response"]
        }
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertFalse(result)
        self.assertEqual(
            error_msg,
            "The secret parameter is invalid or malformed.\n"
            "The response parameter is missing.",
        )

    @mock.patch(imp_requests)
    def test_captcha_false_success(self, requests_mock):
        requests_mock.post().json.return_value = {"success": False}
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertFalse(result)
        self.assertEqual(error_msg, "There was a problem with the captcha entry.")

    @mock.patch(imp_requests)
    def test_captcha_empty_response(self, requests_mock):
        requests_mock.post().json.return_value = {}
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertFalse(result)
        self.assertEqual(error_msg, "There was a problem with the captcha entry.")

    @mock.patch(imp_requests)
    def test_captcha_unknown_error(self, requests_mock):
        requests_mock.post().json.return_value = {"error-codes": ["unknown-error"]}
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertFalse(result)
        self.assertEqual(error_msg, "There was a problem with the captcha entry.")

    @mock.patch(imp_requests)
    def test_captcha_no_errors_and_success(self, requests_mock):
        requests_mock.post().json.return_value = {
            "error-codes": [],
            "success": True,
        }
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertTrue(result)
        self.assertEqual(error_msg, "")

    def test_captcha_no_response(self):
        result, error_msg = self.website.is_captcha_valid({})
        self.assertFalse(result)
        self.assertEqual(error_msg, "No response given.")

    @mock.patch(imp_requests)
    def test_captcha_disabled(self, requests_mock):
        self.env["ir.config_parameter"].sudo().set_param(
            "portal_recaptcha.recaptcha_enabled", False
        )
        result, error_msg = self.website.is_captcha_valid(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertTrue(result)
        self.assertEqual(error_msg, "")
        requests_mock.assert_not_called()
