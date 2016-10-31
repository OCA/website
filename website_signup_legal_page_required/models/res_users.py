# -*- coding: utf-8 -*-
# © 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class User(models.Model):
    _inherit = "res.users"

    accepted_legal_terms = fields.Boolean(
        default=False,
        help="Did the user accept our legal terms when opening the account?")
