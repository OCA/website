# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import requests

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

URL = "https://www.google.com/recaptcha/api/siteverify"


class Website(models.Model):
    _inherit = "website"

    recaptcha_key_site = fields.Char()
    recaptcha_key_secret = fields.Char()

    @api.model
    def _get_error_message(self, errorcode=None):
        mapping = {
            "missing-input-secret": _("The secret parameter is missing."),
            "invalid-input-secret": _("The secret parameter is invalid or malformed."),
            "missing-input-response": _("The response parameter is missing."),
            "invalid-input-response": _(
                "The response parameter is invalid or malformed."
            ),
        }
        return mapping.get(
            errorcode, _("There was a problem with " "the captcha entry.")
        )

    def is_captcha_valid(self, response):
        get_res = {"secret": self.recaptcha_key_secret, "response": response}

        res = requests.post(URL, data=get_res).json()

        error_msg = "\n".join(
            self._get_error_message(error) for error in res.get("error-codes", [])
        )
        if error_msg:
            raise ValidationError(error_msg)

        if not res.get("success"):
            raise ValidationError(self._get_error_message())
        return True
