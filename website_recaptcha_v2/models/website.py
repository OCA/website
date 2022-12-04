# SPDX-FileCopyrightText: 2010-2014 Elico Corp
# SPDX-FileContributor: Augustin Cisterne-Kaas <augustin.cisterne-kaas@elico-corp.com>
# SPDX-FileCopyrightText: 2015 Tech-Receptives Solutions Pvt. Ltd.
# SPDX-FileCopyrightText: 2019 Simone Orsi - Camptocamp SA
# SPDX-FileCopyrightText: 2019 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import requests

from odoo import _, api, fields, models

URL = "https://www.google.com/recaptcha/api/siteverify"


class Website(models.Model):
    _inherit = "website"

    recaptcha_enabled = fields.Boolean("Enable reCAPTCHA")
    recaptcha_key_site = fields.Char("Site Key")
    recaptcha_key_secret = fields.Char("Secret Key")

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
        return mapping.get(errorcode, _("There was a problem with the captcha entry."))

    def is_captcha_valid(self, form_values):
        """
        Checks whether the CAPTCHA has been correctly solved.

        form_values must be a dictionary containing the form values.

        Returns a (bool, str) tuple. The first element tells whether the
        CAPTCHA is valid or not. The second is the error message when
        applicable (or an empty string).

        If reCAPTCHA is disabled in the settings, this method behaves as if
        the CAPTCHA was correctly solved, but without doing any check.
        """
        if not self.recaptcha_enabled:
            return (True, "")
        response = form_values.get("g-recaptcha-response")
        if not response:
            return (False, _("No response given."))
        get_res = {"secret": self.recaptcha_key_secret, "response": response}

        res = requests.post(URL, data=get_res).json()

        error_msg = "\n".join(
            self._get_error_message(error) for error in res.get("error-codes", [])
        )
        if error_msg:
            return (False, error_msg)

        if not res.get("success"):
            return (False, self._get_error_message())
        return (True, "")
