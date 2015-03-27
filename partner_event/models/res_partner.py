# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
from openerp.osv.expression import NEGATIVE_TERM_OPERATORS


class ResPartner(models.Model):
    _inherit = 'res.partner'

    registrations = fields.One2many(
        comodel_name='event.registration', inverse_name="partner_id")
    registration_count = fields.Integer(
        string='Registration number', compute='_count_registration',
        store=True)
    attended_registrations = fields.One2many(
        comodel_name='event.registration',
        compute="_get_attended_registrations",
        search="_search_attended_registrations")
    attended_registration_count = fields.Integer(
        string='Attended registration number',
        compute='_count_attended_registration', store=True)

    @api.one
    @api.depends('registrations')
    def _get_attended_registrations(self):
        self.attended_registrations = self.registrations.filtered(
            lambda x: x.state == 'done')

    def _search_attended_registrations(self, operator, value):
        registration_obj = self.env['event.registration']
        domain = [('state', '=', 'done')]
        if value is not False:
            domain.append((registration_obj._rec_name, operator, value))
        vals = registration_obj.read_group(
            domain, ['partner_id'], ['partner_id'])
        ids = [x['partner_id'][0] for x in vals if x['partner_id']]
        cond = operator in NEGATIVE_TERM_OPERATORS
        if value is False:
            cond = not cond
        if cond:
            return [('id', 'not in', ids)]
        else:
            return [('id', 'in', ids)]

    @api.one
    @api.depends('registrations')
    def _count_registration(self):
        self.registration_count = len(self.registrations)

    @api.one
    @api.depends('attended_registrations')
    def _count_attended_registration(self):
        self.attended_registration_count = len(self.attended_registrations)
