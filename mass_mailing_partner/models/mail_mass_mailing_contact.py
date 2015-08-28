# -*- coding: utf-8 -*-
##############################################################################
# License AGPL-3 - See LICENSE file on root folder for details
##############################################################################

from openerp import models, fields, api


class MailMassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner")
    partner_mandatory = fields.Boolean(related='list_id.partner_mandatory')

    def _prepare_partner(self, vals):
        return {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
            'opt_out': vals.get('opt_out', False),
            'category_id': vals.get('_partner_category'),
        }

    def _check_partner(self, vals, partner_mandatory):
        partner_model = self.env['res.partner']
        # Look for a partner with that email
        partners = partner_model.search([('email', '=ilike', vals['email'])])
        partner_id = False
        if partners:
            partner_id = partners[0].id
        elif partner_mandatory:
            # Create partner
            partner = partner_model.sudo().create(self._prepare_partner(vals))
            partner_id = partner.id
        return partner_id

    @api.model
    def create(self, vals):
        if not vals.get('partner_id') and vals.get('email'):
            mailing_list = self.env['mail.mass_mailing.list'].browse(vals.get(
                'list_id'))
            if mailing_list.partner_mandatory:
                category = mailing_list.partner_category
                if category:
                    vals['_partner_category'] = [(4, category.id, 0)]
            vals['partner_id'] = self._check_partner(vals, partner_mandatory)
            vals.pop('_partner_category')
        return super(MailMassMailingContact, self).create(vals)

    @api.onchange('partner_id')
    def _onchange_partner(self):
        if self.partner_id:
            self.name = self.partner_id.name
            self.email = self.partner_id.email
