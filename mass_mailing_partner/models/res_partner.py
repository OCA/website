# -*- coding: utf-8 -*-
##############################################################################
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    mass_mailing_contacts = fields.One2many(
        comodel_name='mail.mass_mailing.contact', inverse_name='partner_id')

    mass_mailing_contacts_count = fields.Integer(
        string='Mailing list number', compute='_count_mass_mailing_contacts',
        store=True)

    @api.one
    @api.depends('mass_mailing_contacts')
    def _count_mass_mailing_contacts(self):
        self.mass_mailing_contacts_count = len(self.mass_mailing_contacts)

    @api.one
    def write(self, vals):
        self.mass_mailing_contacts.write({
            'name': vals.get('name') or self.name,
            'email': vals.get('email') or self.email
        })
        return super(ResPartner, self).write(vals)
