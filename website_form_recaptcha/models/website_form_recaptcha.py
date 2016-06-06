# -*- coding: utf-8 -*-
# © 2015 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api
from openerp.exceptions import ValidationError
import requests


class WebsiteFormRecaptcha(models.AbstractModel):
    """ This model provides ReCaptcha helper methods.
    Nothing is stored in the DB.
    """

    _name = 'website.form.recaptcha'
    _description = 'Website Form Recaptcha Validations'
    URL = 'https://www.google.com/recaptcha/api/siteverify'
    RESPONSE_ATTR = 'g-recaptcha-response'
    ERROR_MAP = {
        'missing-input-secret': 'The secret parameter is missing.',
        'invalid-input-secret':
            'The secret parameter is invalid or malformed.',
        'missing-input-response': 'The response parameter is missing.',
        'invalid-input-response':
            'The response parameter is invalid or malformed.',
        None: 'There was a problem with the captcha entry.',
    }

    @api.model
    def action_validate(self, response, remote_ip):
        """ Validate ReCaptcha Response
        Params:
            response: str The value of 'g-recaptcha-response'.
            remote_ip: str The end user's IP address
        Raises:
            ValidationError on failure
        Returns:
            True on success
        """

        secret_key = self.env.ref(
            'website_form_recaptcha.recaptcha_key_secret'
        )
        secret_key = secret_key.sudo().value

        # @TODO: Domain validation
        # domain_name = request.httprequest.environ.get(
        #     'HTTP_HOST', ''
        # ).split(':')[0]

        data = {
            'secret': secret_key,
            'response': response,
            'remoteip': remote_ip,
        }
        res = requests.post(self.URL, data=data).json()

        for error in res.get('error-codes', []):
            raise ValidationError(
                self.ERROR_MAP.get(
                    error, self.ERROR_MAP[None]
                )
            )

        if not res.get('success'):
            raise ValidationError(self.ERROR_MAP[None])

        return True
