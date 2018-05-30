# -*- coding: utf-8 -*-
# Copyright 2015 Tecnativa
# Copyright 2016 Alessio Gerace - Agile Business Group
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
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
