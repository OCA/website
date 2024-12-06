import json
from unittest import mock

from odoo import http
from odoo.http import Response
from odoo.tests import new_test_user
from odoo.tests.common import HttpCase

from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS
from odoo.addons.website_recaptcha_v2_form.controllers.form import WebsiteRecaptchaForm
from odoo.addons.website_recaptcha_v2_form.controllers.main import (
    RecaptchaAuthSignupHome,
)

addons_controller = "odoo.addons.website_recaptcha_v2_form.controllers"

patch_signup = addons_controller + ".main.RecaptchaAuthSignupHome.web_auth_signup"


class TestControllerForm(HttpCase):
    def test_url_open(self, data=None, url="/website/form/res.partner"):
        if not data:
            data = {
                "recaptcha_enabled": True,
                "g-recaptcha": "",
            }
        res = self.url_open(
            url=url,
            data=data,
        )
        return res

    def test_recaptcha_enabled_form(self):
        response = self.test_url_open()
        response_recaptcha_invalid = json.loads(response.content.decode("utf-8"))
        self.assertEqual(
            response_recaptcha_invalid.get("error"),
            "No response given.",
            msg=response_recaptcha_invalid.get("error"),
        )
        response_recaptcha_not_enable = self.test_url_open(
            data={"recaptcha_enabled": False}
        )
        self.assertEqual(response_recaptcha_not_enable.status_code, 200)

        response_recaptcha_not_enable = self.test_url_open(data={})
        self.assertEqual(response_recaptcha_not_enable.status_code, 200)

    def test_recaptcha_enabled_reset_password_login_signup(self):
        new_test_user(self.env, login="test_user_form", password="Password!1")
        self.authenticate("test_user_form", "Password!1")
        data = {
            "csrf_token": http.Request.csrf_token(self),
            "g-recaptcha-response": "recaptcha_invalid",
        }
        response_reset = self.test_url_open(url="/web/reset_password", data=data)
        self.assertEqual(response_reset.status_code, 200)

        data.update(
            {
                "login": "test_user_form",
                "password": "Password!1",
            }
        )
        response = self.test_url_open(url="/web/login", data=data)
        self.assertEqual(response.status_code, 200)

        SIGN_UP_REQUEST_PARAMS.add("confirm_password")
        response = self.test_url_open(url="/web/login", data=data)
        self.assertEqual(response.status_code, 200)

    @mock.patch(
        "odoo.addons.website_recaptcha_v2_form.controllers.form.WebsiteForm.website_form"
    )
    def test_success_form(self, mock_super_website_form):
        mock_super_website_form.return_value = Response("Success")

        form_controller = WebsiteRecaptchaForm()
        response = form_controller.website_form(
            model_name="res.partner",
            recaptcha_enabled=False,
            **{"test_key": "test_value"},
        )
        self.assertEqual(response.status_code, 200)

    @mock.patch(patch_signup)
    def test_recaptcha_disabled(self, mock_super_website_form):
        mock_super_website_form.return_value = "Not boolean"
        form_controller = RecaptchaAuthSignupHome()
        response = form_controller.web_auth_signup(
            *{},
            **{},
        )
        self.assertEqual(response, "Not boolean")
