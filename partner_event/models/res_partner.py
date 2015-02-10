# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registrations = fields.One2many(
        comodel_name='event.registration', inverse_name="partner_id")
    registration_count = fields.Integer(
        string='Registration number', compute='_count_registration')

    @api.one
    @api.depends('registrations')
    def _count_registration(self):
        self.registration_count = len(self.registrations)
