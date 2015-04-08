# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#    Copyright (c) 2015 Antiun Ingeniería S.L.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class MailMassMailingContact(models.Model):
    _inherit = 'mail.mass_mailing.contact'

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner")

    def _prepare_partner(self, vals):
        return {
            'name': vals.get('name') or vals.get('email'),
            'email': vals.get('email', False),
            'opt_out': vals.get('opt_out', False),
        }

    def _check_partner(self, vals):
        partner_model = self.env['res.partner']
        # Look for a partner with that email
        partners = partner_model.search([('email', '=ilike', vals['email'])])
        if partners:
            partner_id = partners[0].id
        else:
            # Create partner
            partner = partner_model.sudo().create(self._prepare_partner(vals))
            partner_id = partner.id
        return partner_id

    @api.model
    def create(self, vals):
        if not vals.get('partner_id') and vals.get('email'):
            vals['partner_id'] = self._check_partner(vals)
        return super(MailMassMailingContact, self).create(vals)

    @api.multi
    def write(self, vals):
        # Synchronize opt_out value
        if vals.get('opt_out') is not None:
            recs = self.filtered(lambda x: x.partner_id)
            for contact in recs:
                if contact.partner_id.opt_out != vals['opt_out']:
                    contact.partner_id.opt_out = vals['opt_out']
        if not vals.get('partner_id') and vals.get('email'):
            vals['partner_id'] = self._check_partner(vals)
        return super(MailMassMailingContact, self).write(vals)
