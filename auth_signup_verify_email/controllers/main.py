# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging
from openerp import _, http
from openerp.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)


class SignupVerifyEmail(AuthSignupHome):
    def _signup_with_values(self, token, values):
        values["password"] = False
        qcontext = self.get_auth_signup_qcontext()
        sudo_users = http.request.env["res.users"].sudo()

        try:
            sudo_users.signup(values, token)
            sudo_users.reset_password(values.get("login"))
        except Exception as error:
            # Duplicate key or wrong SMTP settings, probably
            _logger.exception(error)

            # Agnostic message for security
            qcontext["error"] = _(
                "Something went wrong, please try again later or contact us.")
            return http.request.render("auth_signup.signup", qcontext)

        qcontext["message"] = _("Check your email to activate your account!")
        return http.request.render("auth_signup.reset_password", qcontext)
