# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json

from odoo import http

from odoo.addons.website.controllers.form import WebsiteForm

from .main import RecaptchaHome


class WebsiteRecaptchaForm(WebsiteForm):
    @http.route(
        "/website/form/<string:model_name>",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=False,
    )
    def website_form(self, model_name, **kwargs):
        if kwargs.get("recaptcha_enabled", False):
            valid = RecaptchaHome.verify_recaptcha_v2(self, values=kwargs)
            if not isinstance(valid, bool):
                return json.dumps(
                    {
                        "error": valid,
                    }
                )
        return super().website_form(model_name, **kwargs)
