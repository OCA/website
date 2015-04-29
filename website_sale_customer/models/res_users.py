# -*- coding: utf-8 -*-

from openerp import models
from openerp import api
from openerp.tools.translate import _

from openerp.addons.auth_signup.res_users import SignupError

from openerp.addons.website_sale_customer import utils


INVALID_EMAIL_MSG = _("Invalid email! "
                      "Please, provide a valid and existing email.")

USER_EXISTS_MSG = _("Sorry, this email / login is not available. "
                    "Are you already registered?")


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _signup_create_user(self, cr, uid, values, context=None):
        """ Override to validate data before creating user.
        """

        self._validate_signup_values(cr, uid, values, context=context)
        return super(ResUsers, self)._signup_create_user(cr, uid, values,
                                                         context=context)

    def _validate_signup_values(self, cr, uid, values, context=None):
        login = values.get('login')
        email = values.get('email')
        email = email or login
        if not utils.validate_email(email):
            raise SignupError(INVALID_EMAIL_MSG)
        # raise proper error if user exists
        # instead of throwing
        # duplicate key value violates unique constraint
        #   "res_users_login_key" DETAIL:
        #        Key (login)=(LOGIN_HERE) already exists.
        ids = self.search(cr, uid, [('login', '=', login or email)])
        if ids:
            raise SignupError(USER_EXISTS_MSG)

    def _get_default_action(self):
        return self.env.ref('website_sale_customer.default_home_action')

    @api.model
    def create(self, vals):
        if not vals.get('action_id'):
            action = self._get_default_action()
            vals['action_id'] = action and action.id or False
        return super(ResUsers, self).create(vals)
