# -*- coding: utf-8 -*-
# Copyright 2015 Tecnativa
# Copyright 2016 Alessio Gerace - Agile Business Group
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo.addons.auth_signup.models.res_partner import SignupError


class LegalTermsNotAcceptedError(SignupError):
    def __init__(self, msg=None):
        msg = msg or _("You must accept our legal terms.")
        super(LegalTermsNotAcceptedError, self).__init__(msg)
