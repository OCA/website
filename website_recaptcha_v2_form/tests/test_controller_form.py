import json
from unittest import mock

from odoo import http
from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase
from odoo.tools.misc import hmac

imp_requests = "odoo.addons.website_recaptcha_v2.models.website.requests"


@tagged("post_install", "-at_install")
class TestControllerForm(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["website"].search([]).write(
            {
                "recaptcha_v2_enabled": True,
                "recaptcha_v2_site_key": "test-site",
                "recaptcha_v2_secret_key": "test-secret",
            }
        )
        cls.env["website"].search([]).write({"auth_signup_uninvited": "b2c"})
        cls.env["ir.config_parameter"].sudo().set_param(
            "auth_signup.reset_password", True
        )
        cls.user = new_test_user(cls.env, login="test_user_form", password="Password!1")

    def setUp(self):
        super().setUp()
        self.authenticate(None, None)
        patcher = mock.patch(imp_requests)
        self.requests_mock = patcher.start()
        self.addCleanup(patcher.stop)
        self._set_recaptcha_success(False)

    def _set_recaptcha_success(self, success):
        self.requests_mock.post.return_value.json.return_value = {"success": success}

    def _post(self, url, data):
        data = dict(data, csrf_token=http.Request.csrf_token(self))
        return self.url_open(url, data=data)

    def _post_form(self, data):
        response = self.url_open("/website/form/mail.mail", data=data)
        self.assertEqual(response.status_code, 200)
        return json.loads(response.content.decode("utf-8"))

    def _mail_values(self):
        return {
            "email_to": "test@example.com",
            "subject": "Test recaptcha",
            "website_form_signature": hmac(
                self.env(su=True), "website_form_signature", "test@example.com"
            ),
        }

    def test_form_recaptcha_missing_response(self):
        result = self._post_form({"recaptcha_enabled": True})
        self.assertEqual(result.get("error"), "No response given.")
        self.requests_mock.post.assert_not_called()

    def test_form_recaptcha_invalid(self):
        result = self._post_form(
            {"recaptcha_enabled": True, "g-recaptcha-response": "invalid"}
        )
        self.assertEqual(
            result.get("error"), "The challenge was not successfully completed."
        )

    def test_form_recaptcha_valid(self):
        self._set_recaptcha_success(True)
        result = self._post_form(
            dict(
                self._mail_values(),
                recaptcha_enabled=True,
                **{"g-recaptcha-response": "valid"},
            )
        )
        self.assertNotIn("error", result)
        self.assertTrue(result.get("id"))
        self.requests_mock.post.assert_called_once()

    def test_form_recaptcha_not_enabled(self):
        result = self._post_form(self._mail_values())
        self.assertNotIn("error", result)
        self.assertTrue(result.get("id"))
        self.requests_mock.post.assert_not_called()

    def test_login_recaptcha_invalid(self):
        response = self._post(
            "/web/login",
            {
                "login": "test_user_form",
                "password": "Password!1",
                "g-recaptcha-response": "invalid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("The challenge was not successfully completed.", response.text)
        self.assertEqual(response.headers.get("X-Frame-Options"), "SAMEORIGIN")
        self.assertFalse(self.session.uid)

    def test_login_recaptcha_valid(self):
        self._set_recaptcha_success(True)
        response = self._post(
            "/web/login",
            {
                "login": "test_user_form",
                "password": "Password!1",
                "g-recaptcha-response": "valid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("The challenge was not successfully completed.", response.text)
        self.requests_mock.post.assert_called_once()

    def test_login_from_signup_skips_recaptcha(self):
        response = self._post(
            "/web/login",
            {
                "login": "test_user_form",
                "password": "Password!1",
                "confirm_password": "Password!1",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.requests_mock.post.assert_not_called()

    def test_reset_password_get(self):
        response = self.url_open("/web/reset_password")
        self.assertEqual(response.status_code, 200)
        self.requests_mock.post.assert_not_called()

    def test_reset_password_recaptcha_invalid(self):
        response = self._post(
            "/web/reset_password",
            {"login": "test_user_form", "g-recaptcha-response": "invalid"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("The challenge was not successfully completed.", response.text)

    def test_reset_password_recaptcha_valid(self):
        self._set_recaptcha_success(True)
        response = self._post(
            "/web/reset_password",
            {"login": "test_user_form", "g-recaptcha-response": "valid"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("The challenge was not successfully completed.", response.text)
        self.requests_mock.post.assert_called_once()

    def test_signup_get(self):
        response = self.url_open("/web/signup")
        self.assertEqual(response.status_code, 200)
        self.requests_mock.post.assert_not_called()

    def test_signup_recaptcha_invalid(self):
        response = self._post(
            "/web/signup",
            {
                "login": "new_user_form@example.com",
                "name": "New user form",
                "password": "Password!1",
                "confirm_password": "Password!1",
                "g-recaptcha-response": "invalid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("The challenge was not successfully completed.", response.text)
        self.assertFalse(
            self.env["res.users"].search([("login", "=", "new_user_form@example.com")])
        )

    def test_signup_recaptcha_valid(self):
        self._set_recaptcha_success(True)
        response = self._post(
            "/web/signup",
            {
                "login": "new_user_form@example.com",
                "name": "New user form",
                "password": "Password!1",
                "confirm_password": "Password!1",
                "g-recaptcha-response": "valid",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            self.env["res.users"].search([("login", "=", "new_user_form@example.com")])
        )
        self.requests_mock.post.assert_called_once()
