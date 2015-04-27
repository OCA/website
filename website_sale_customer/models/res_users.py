# -*- coding: utf-8 -*-

from openerp import models
from openerp.tools.translate import _

from openerp.addons.auth_signup.res_users import SignupError

from openerp.addons.website_sale_customer import utils


INVALID_EMAIL_MSG = _("Invalid email! "
                      "Please, provide a valid and existing email.")


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _signup_create_user(self, cr, uid, values, context=None):
        """ Override to validate data before creating user.
        """

        self._validate_signup_values(cr, uid, values, context=context)
        return super(ResUsers, self)._signup_create_user(cr, uid, values,
                                                         context=context)

    def _validate_signup_values(self, cr, uid, values, context=None):
        email = values.get('login') or values.get('email')
        if not utils.validate_email(email):
            raise SignupError(INVALID_EMAIL_MSG)
