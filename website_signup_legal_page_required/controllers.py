# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.http import request
from openerp.addons.auth_signup.controllers.main import AuthSignupHome
from . import exceptions


class ForceLegalTerms(AuthSignupHome):
    def _signup_with_values(self, token, values, *args, **kwargs):
        """Force accepting legal terms to open an account."""
        if request.params.get("accepted_legal_terms"):
            values["accepted_legal_terms"] = True
            return super(ForceLegalTerms, self)._signup_with_values(
                token, values, *args, **kwargs)
        else:
            raise exceptions.LegalTermsNotAcceptedError()
