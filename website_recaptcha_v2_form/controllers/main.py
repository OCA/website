import logging

from odoo import _, http
from odoo.exceptions import AccessDenied
from odoo.http import request

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS, Home

logger = logging.getLogger(__name__)

SIGN_UP_REQUEST_PARAMS.add("g-recaptcha-response")


class RecaptchaHome(Home):
    def verify_recaptcha_v2(self, kw=None, template="", values=None):
        Website = request.env["website"].sudo()
        try:
            request.env["ir.http"]._auth_method_public()
            valid = Website.get_current_website().valid_recaptcha(values)
            if valid:
                if template == "web.login":
                    return super().web_login(values.get("redirect", ""), **kw)
                else:
                    return True
        except AccessDenied as e:
            message_error = str(
                e.args[0] if len(e.args) > 0 else _("Recaptcha is not valid.")
            )
            if template in (
                "web.login",
                "auth_signup.reset_password",
                "auth_signup.signup",
            ):
                values.update({"error": message_error})
                response = request.render(template, values)
                response.headers["X-Frame-Options"] = "SAMEORIGIN"
                response.headers["Content-Security-Policy"] = "frame-ancestors 'self'"
                return response
            else:
                return message_error

    @http.route("/web/login", type="http", auth="none")
    def web_login(self, redirect=None, **kw):
        if request.httprequest.method == "POST":
            values = {
                k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS
            }
            # Checking that if the request comes from the creation of the account,
            # that the recaptcha is not checked again to avoid errors.

            if (
                values.get("confirm_password", "") == ""
                and request.httprequest.url.find("web/signup") == -1
            ):
                return self.verify_recaptcha_v2(
                    kw=kw, template="web.login", values=values
                )
        return super().web_login(redirect, **kw)


class RecaptchaAuthSignupHome(AuthSignupHome):
    @http.route(
        "/web/reset_password", type="http", auth="public", website=True, sitemap=False
    )
    def web_auth_reset_password(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if request.httprequest.method == "POST":
            valid = self.verify_recaptcha_v2(
                kw=kw, template="auth_signup.reset_password", values=qcontext
            )
            if not isinstance(valid, bool):
                return valid
        return super().web_auth_reset_password(*args, **kw)

    @http.route("/web/signup", type="http", auth="public", website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if request.httprequest.method == "POST":
            valid = self.verify_recaptcha_v2(
                template="auth_signup.signup", values=qcontext
            )
            if not isinstance(valid, bool):
                return valid
        return super().web_auth_signup(*args, **kw)
