import re

import odoo
from odoo.tests import HOST
from odoo.tests.common import HttpCase

from odoo.addons.mail.tests.common import mail_new_test_user


class TestControllerFormCommon(HttpCase):
    def setUp(self):
        super().setUp()
        self.website1 = (
            self.env["website"]
            .sudo()
            .create(
                {
                    "name": "Test Website",
                    "recaptcha_v2_enabled": True,
                    "recaptcha_v2_site_key": "test_site_key",
                    "recaptcha_v2_secret_key": "test_secret_key",
                }
            )
        )
        self.test_values = {"recaptcha_token": "test_token"}
        self.test_kw = {"some_key": "some_value"}
        self.user_recaptcha = mail_new_test_user(
            self.env,
            groups="base.group_user,base.group_system,website.group_website_designer",
            login="user_recaptcha",
            name="User Recaptcha",
            signature="--\nRecaptcha",
        )
        self.csrf_token = self._get_csrf_token()
        self.reset_pass_values = {
            "name": self.user_recaptcha.name,
            "email": self.user_recaptcha.email,
            "csrf_token": self.csrf_token,
            "reset_password_enabled": True,
        }
        self.signup_values = {
            "csrf_token": self.csrf_token,
            "signup_enabled": True,
            "login": "user_test",
            "name": "User test",
        }

    def test_url_open(self, data=None, url="/website/form/res.partner"):
        if not data:
            data = {
                "recaptcha_enabled": True,
                "g-recaptcha": "",
            }
        res = self.url_open(url=url, data=data)
        return res

    def _get_csrf_token(self):
        body = self.test_url_open(
            url=f"http://{HOST}:{odoo.tools.config['http_port']}/web/signup"
        ).text
        csrf = re.search(r'csrf_token: "(\w*?)"', body).group(1)
        return csrf
