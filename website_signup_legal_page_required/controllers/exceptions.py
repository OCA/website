# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import _
from openerp.addons.auth_signup.res_users import SignupError


class LegalTermsNotAcceptedError(SignupError):
    def __init__(self, msg=_("You must accept our legal terms.")):
        super(LegalTermsNotAcceptedError, self).__init__(msg)
