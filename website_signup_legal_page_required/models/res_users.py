# -*- coding: utf-8 -*-
# Copyright 2015 Tecnativa
# Copyright 2016 Alessio Gerace - Agile Business Group
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class User(models.Model):
    _inherit = "res.users"

    accepted_legal_terms = fields.Boolean(
        default=False,
        help="Did the user accept our legal terms when opening the account?")
