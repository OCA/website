# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_ref_unique = fields.Selection(
        selection=[
            ('none', 'None'),
            ('companies', 'Only companies'),
            ('all', 'All partners'),
        ], string="Unique partner reference for", default="none")
