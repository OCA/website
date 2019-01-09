# Copyright 2015-2017 LasLabs Inc.
# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, http, _
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

    def _get_api_params(self):
        ICP = self.env['ir.config_parameter'].sudo()
        return {
            'site_key': ICP.get_param('recaptcha.key.site'),
            'secret_key': ICP.get_param('recaptcha.key.secret'),
        }

    def _get_api_credentials(self, website=None):
        # defaults
        params = self._get_api_params()
        # website override
        website = website or http.request.website
        site_key = website.recaptcha_key_site or params['site_key']
        secret_key = website.recaptcha_key_secret or params['secret_key']
        return {
            'site_key': site_key,
            'secret_key': secret_key,
        }

    @api.model
    def validate_response(self, response, remote_ip, website=None):
        """ Validate ReCaptcha Response
        Params:
            response: str The value of 'g-recaptcha-response'.
            remote_ip: str The end user's IP address
        Raises:
            ValidationError on failure
        Returns:
            True on success
        """

        # @TODO: Domain validation
        # domain_name = request.httprequest.environ.get(
        #     'HTTP_HOST', ''
        # ).split(':')[0]
        creds = self._get_api_credentials(website=website)
        data = {
            'secret': creds['secret_key'],
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

    @api.model
    def validate_request(self, request, values):
        # Only check once: if a call to reCAPTCHA's API is made twice with
        # the same token, we get a 'timeout-or-duplicate' error. So we
        # stick to the first response data storing the token after the
        # first invoke in the current request object. This duplicated
        # call can be cause for instance by website_crm_phone_validation.
        try:
            getattr(request, self.RESPONSE_ATTR)
        except AttributeError:
            return None
        ip_addr = request.httprequest.environ.get('HTTP_X_FORWARDED_FOR')
        if ip_addr:
            ip_addr = ip_addr.split(',')[0]
        else:
            ip_addr = request.httprequest.remote_addr
        try:
            self.validate_response(
                values.get(self.RESPONSE_ATTR), ip_addr
            )
            # Store reCAPTCHA's token in the current request object
            setattr(
                request, self.RESPONSE_ATTR, values.get(self.RESPONSE_ATTR)
            )
        except ValidationError:
            raise ValidationError([self.RESPONSE_ATTR])
