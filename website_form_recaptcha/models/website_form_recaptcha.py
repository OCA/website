# Copyright 2015-2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, _
from odoo.exceptions import ValidationError
import requests


class WebsiteFormRecaptcha(models.AbstractModel):
    """ This model provides ReCaptcha helper methods.
    Nothing is stored in the DB.
    """

    _name = 'website.form.recaptcha'
    _description = 'Website Form Recaptcha Validations'
    URL = 'https://www.google.com/recaptcha/api/siteverify'
    RESPONSE_ATTR = 'g-recaptcha-response'

    @api.model
    def _get_error_message(self, errorcode=None):
        map = {
            'missing-input-secret': _('The secret parameter is missing.'),
            'invalid-input-secret':
                _('The secret parameter is invalid or malformed.'),
            'missing-input-response': _('The response parameter is missing.'),
            'invalid-input-response':
                _('The response parameter is invalid or malformed.'),
        }
        return map.get(errorcode, _('There was a problem with '
                                    'the captcha entry.'))

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

        ICP = self.env['ir.config_parameter'].sudo()
        secret_key = ICP.get_param('recaptcha.key.secret')

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

        error_msg = "\n".join(self._get_error_message(error)
                              for error in res.get('error-codes', []))
        if error_msg:
            raise ValidationError(error_msg)

        if not res.get('success'):
            raise ValidationError(self._get_error_message())

        return True
