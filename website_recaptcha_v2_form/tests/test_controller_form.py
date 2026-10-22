from unittest import mock

from odoo.tests.common import users

from .test_controller_form_http_common import TestControllerFormCommon

addons_controller = "odoo.addons.website_recaptcha_v2_form.controllers"
addons_models = "odoo.addons.website_recaptcha_v2_form.models"
patch_verify_recaptcha_v2 = (
    addons_controller + ".main.RecaptchaHome.verify_recaptcha_v2"
)
patch_login_redirect = addons_controller + ".main.RecaptchaHome._login_redirect"
patch_valid_recaptcha = addons_models + ".website.Website.valid_recaptcha"
patch_signup = addons_controller + ".main.RecaptchaAuthSignupHome.web_auth_signup"
patch_login = addons_controller + ".main.RecaptchaHome.web_login"
patch_request = addons_controller + ".main.request"
patch_recaptchahome = addons_controller + ".main.RecaptchaHome"

addons_auth_signup = "odoo.addons.auth_signup"
patch_signup_qcontext = (
    addons_auth_signup + ".controllers.main.AuthSignupHome.get_auth_signup_qcontext"
)


class TestControllerForm(TestControllerFormCommon):
    def setUp(self):
        super().setUp()

    @mock.patch(patch_login)
    @mock.patch(patch_signup_qcontext)
    @mock.patch(patch_valid_recaptcha)
    @mock.patch(patch_verify_recaptcha_v2)
    @users("user_recaptcha")
    def test_verify_return_login(
        self,
        mock_verify_recaptcha,
        mock_valid_recaptcha,
        mock_signup_qcontext,
        mock_login,
    ):
        mock_valid_recaptcha.return_value = True
        mock_login.return_value = True
        mock_verify_recaptcha.return_value = mock_login()
        mock_signup_qcontext.return_value = self.reset_pass_values
        response = self.test_url_open(
            url="/web/reset_password", data=self.reset_pass_values
        )
        self.assertEqual(response.status_code, 200)
        mock_login.assert_called_once()

        self.assertEqual(mock_signup_qcontext.call_count, 2)

    @mock.patch(patch_signup_qcontext)
    @mock.patch(patch_verify_recaptcha_v2)
    @users("user_recaptcha")
    def test_reset_password(self, mock_verify_recaptcha, mock_signup_qcontext):
        mock_verify_recaptcha.return_value = True
        mock_signup_qcontext.return_value = self.reset_pass_values
        response = self.test_url_open(
            url="/web/reset_password", data=self.reset_pass_values
        )
        self.assertEqual(response.status_code, 200)
        mock_verify_recaptcha.assert_called_once()
        self.assertEqual(mock_signup_qcontext.call_count, 2)

    @mock.patch(patch_signup_qcontext)
    @mock.patch(patch_verify_recaptcha_v2)
    @users("user_recaptcha")
    def test_reset_password_invalid(self, mock_verify_recaptcha, mock_signup_qcontext):
        mock_verify_recaptcha.return_value = False
        mock_signup_qcontext.return_value = {}
        response = self.test_url_open(url="/web/reset_password", data={})
        self.assertEqual(response.status_code, 400)

        mock_signup_qcontext.return_value = self.reset_pass_values
        response = self.test_url_open(
            url="/web/reset_password", data=self.reset_pass_values
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch(patch_signup_qcontext)
    @mock.patch(patch_verify_recaptcha_v2)
    def test_web_auth_signup(self, mock_verify_recaptcha, mock_signup_qcontext):
        mock_verify_recaptcha.return_value = True
        mock_signup_qcontext.return_value = self.signup_values
        response = self.test_url_open(url="/web/signup", data=self.signup_values)
        self.assertEqual(response.status_code, 200)
        mock_verify_recaptcha.assert_called_once()
        self.assertEqual(mock_signup_qcontext.call_count, 2)

    @mock.patch(patch_signup_qcontext)
    @mock.patch(patch_verify_recaptcha_v2)
    @users("user_recaptcha")
    def test_web_auth_signup_invalid(self, mock_verify_recaptcha, mock_signup_qcontext):
        mock_verify_recaptcha.return_value = False
        mock_signup_qcontext.return_value = {}
        response = self.test_url_open(url="/web/signup", data={})
        self.assertEqual(response.status_code, 400)

        mock_signup_qcontext.return_value = self.signup_values
        response = self.test_url_open(url="/web/signup", data=self.signup_values)
        self.assertEqual(response.status_code, 200)

    @mock.patch(patch_verify_recaptcha_v2)
    @mock.patch(patch_login_redirect)
    @mock.patch(patch_recaptchahome)
    def test_login_redirect(
        self, mock_recaptchahome, mock_login_redirect, mock_verify_recaptcha_v2
    ):
        mock_login_redirect.values = {
            "csrf_token": self.csrf_token,
            "redirect": "/web/test",
            "confirm_password": "",
        }
        mock_login_redirect.valid = True
        mock_verify_recaptcha_v2.return_value = True
        mock_login_redirect.request.httprequest.url = "/web/login"
        mock_recaptchahome._login_redirect.return_value = mock_login_redirect
        result = mock_recaptchahome._login_redirect(
            uid=self.user_recaptcha.id, redirect="/web/test"
        )
        self.assertEqual(result, mock_login_redirect)
        self.assertEqual(mock_login_redirect.values["redirect"], "/web/test")
        self.assertTrue(mock_login_redirect.valid)
