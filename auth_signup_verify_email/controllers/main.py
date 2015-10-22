# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _, http
from openerp.addons.auth_signup.controllers.main import AuthSignupHome


class SignupVerifyEmail(AuthSignupHome):
    def _signup_with_values(self, token, values):
        values["password"] = False
        sudo_users = http.request.env["res.users"].sudo()
        sudo_users.signup(values, token)
        sudo_users.reset_password(values.get("login"))
        return http.request.render(
            "auth_signup.reset_password",
            {"message": _("Check your email to activate your account!")})
