# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.auth_signup.controllers.main import AuthSignupHome
from openerp.http import request


class AuthSignupHome(AuthSignupHome):

    def do_signup(self, qcontext):
        """ Shared helper that creates a res.partner out of a token """
        values = dict(
            (key, qcontext.get(key)) for key in (
                'login', 'name', 'password', 'account_type'))
        assert any([k for k in values.values()]),\
            "The form was not properly filled in."
        assert values.get('password') == qcontext.get('confirm_password'),\
            "Passwords do not match; please retype them."
        values['lang'] = request.lang
        self._signup_with_values(qcontext.get('token'), values)
        request.cr.commit()
