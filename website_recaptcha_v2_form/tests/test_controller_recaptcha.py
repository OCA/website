import json
import re
from unittest import mock

from odoo import http
from odoo.tests import new_test_user, tagged
from odoo.tests.common import HttpCase
from odoo.tools.misc import hmac

from odoo.addons.website_recaptcha_v2.models.website import RECAPTCHA_API_URL

patch_requests_post = "odoo.addons.website_recaptcha_v2.models.website.requests.post"


@tagged("post_install", "-at_install")
class TestControllerRecaptcha(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["website"].search([]).write(
            {
                "recaptcha_v2_enabled": True,
                "recaptcha_v2_site_key": "test-site",
                "recaptcha_v2_secret_key": "test-secret",
                "auth_signup_uninvited": "b2c",
            }
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "auth_signup.reset_password", "True"
        )
        cls.user = new_test_user(
            cls.env,
            login="recaptcha_user",
            password="recaptcha_user_pwd",
            email="recaptcha_user@example.com",
        )

    def _mock_siteverify(self, success=True):
        response = mock.Mock()
        response.json.return_value = {"success": success}
        return mock.patch(patch_requests_post, return_value=response)

    def _assert_siteverify_called(self, mock_post, token="valid-token"):
        mock_post.assert_called_once()
        self.assertEqual(mock_post.call_args.args, (RECAPTCHA_API_URL,))
        self.assertEqual(
            mock_post.call_args.kwargs["data"],
            {"secret": "test-secret", "response": token},
        )

    def _get_csrf_token(self, url):
        body = self.url_open(url).text
        return re.search(r'name="csrf_token" value="([^"]+)"', body).group(1)

    def _session_uid(self):
        sid = self.opener.cookies["session_id"]
        return http.root.session_store.get(sid).uid

    def _post_form(self, **values):
        data = {
            "email_to": "to@example.com",
            "website_form_signature": hmac(
                self.env(su=True), "website_form_signature", "to@example.com"
            ),
        }
        data.update(values)
        return self.url_open("/website/form/mail.mail", data=data)

    def _post_login(self, **values):
        data = {
            "csrf_token": self._get_csrf_token("/web/login"),
            "login": self.user.login,
            "password": "recaptcha_user_pwd",
        }
        data.update(values)
        return self.url_open("/web/login", data=data, allow_redirects=False)

    def _post_reset_password(self, **values):
        data = {
            "csrf_token": self._get_csrf_token("/web/reset_password"),
            "login": self.user.login,
        }
        data.update(values)
        return self.url_open("/web/reset_password", data=data)

    def _post_signup(self, **values):
        data = {
            "csrf_token": self._get_csrf_token("/web/signup"),
            "login": "recaptcha_signup@example.com",
            "name": "Recaptcha Signup",
            "password": "recaptcha_signup_pwd",
            "confirm_password": "recaptcha_signup_pwd",
        }
        data.update(values)
        return self.url_open("/web/signup", data=data, allow_redirects=False)

    def _assert_security_headers(self, response):
        self.assertEqual(response.headers["X-Frame-Options"], "SAMEORIGIN")
        self.assertEqual(
            response.headers["Content-Security-Policy"], "frame-ancestors 'self'"
        )

    def test_website_form_without_recaptcha(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_form(subject="No recaptcha")
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()
        mail = self.env["mail.mail"].browse(json.loads(response.text)["id"])
        self.assertEqual(mail.subject, "No recaptcha")

    def test_website_form_recaptcha_valid(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_form(
                **{
                    "recaptcha_enabled": "True",
                    "g-recaptcha-response": "valid-token",
                    "subject": "Valid recaptcha",
                }
            )
        self.assertEqual(response.status_code, 200)
        self._assert_siteverify_called(mock_post)
        mail = self.env["mail.mail"].browse(json.loads(response.text)["id"])
        self.assertEqual(mail.subject, "Valid recaptcha")

    def test_website_form_recaptcha_not_solved(self):
        with self._mock_siteverify(success=False) as mock_post:
            response = self._post_form(
                **{
                    "recaptcha_enabled": "True",
                    "g-recaptcha-response": "invalid-token",
                    "subject": "Invalid recaptcha",
                }
            )
        self.assertEqual(response.status_code, 200)
        self._assert_siteverify_called(mock_post, token="invalid-token")
        self.assertEqual(
            json.loads(response.text),
            {"error": "The challenge was not successfully completed."},
        )
        self.assertFalse(
            self.env["mail.mail"].search([("subject", "=", "Invalid recaptcha")])
        )

    def test_login_get(self):
        with self._mock_siteverify() as mock_post:
            response = self.url_open("/web/login")
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()

    def test_login_recaptcha_valid(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_login(**{"g-recaptcha-response": "valid-token"})
        self.assertEqual(response.status_code, 303)
        self._assert_siteverify_called(mock_post)
        self.assertEqual(self._session_uid(), self.user.id)

    def test_login_recaptcha_missing(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_login()
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()
        self.assertIn("No response given.", response.text)
        self._assert_security_headers(response)
        self.assertFalse(self._session_uid())

    def test_reset_password_get(self):
        with self._mock_siteverify() as mock_post:
            response = self.url_open("/web/reset_password")
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()

    def test_reset_password_recaptcha_valid(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_reset_password(
                **{"g-recaptcha-response": "valid-token"}
            )
        self.assertEqual(response.status_code, 200)
        self._assert_siteverify_called(mock_post)
        self.assertIn("Password reset instructions sent to your email", response.text)

    def test_reset_password_recaptcha_missing(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_reset_password()
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()
        self.assertIn("No response given.", response.text)
        self.assertNotIn(
            "Password reset instructions sent to your email", response.text
        )
        self._assert_security_headers(response)

    def test_signup_get(self):
        with self._mock_siteverify() as mock_post:
            response = self.url_open("/web/signup")
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()

    def test_signup_recaptcha_valid(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_signup(**{"g-recaptcha-response": "valid-token"})
        self.assertEqual(response.status_code, 303)
        # The login performed by the signup does not check the recaptcha again.
        self._assert_siteverify_called(mock_post)
        new_user = self.env["res.users"].search(
            [("login", "=", "recaptcha_signup@example.com")]
        )
        self.assertTrue(new_user)
        self.assertEqual(self._session_uid(), new_user.id)

    def test_signup_recaptcha_missing(self):
        with self._mock_siteverify() as mock_post:
            response = self._post_signup()
        self.assertEqual(response.status_code, 200)
        mock_post.assert_not_called()
        self.assertIn("No response given.", response.text)
        self._assert_security_headers(response)
        self.assertFalse(
            self.env["res.users"].search(
                [("login", "=", "recaptcha_signup@example.com")]
            )
        )
