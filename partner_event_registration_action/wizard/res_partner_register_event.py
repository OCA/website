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


class ResPartnerRegisterEvent(models.TransientModel):
    _name = 'res.partner.register.event'

    event = fields.Many2one('event.event', required=True)
    ticket = fields.Many2one(
        'event.event.ticket', required=True,
        domain="[('event_id', '=', event)]")

    def _prepare_registration(self, partner):
        return {
            'event_id': self.event.id,
            'event_ticket_id': self.ticket.id,
            'partner_id': partner.id,
            'nb_register': 1,
            'name': partner.name,
            'email': partner.email,
            'phone': partner.phone,
            'date_open': fields.Datetime.now(),
        }

    @api.multi
    def button_register(self):
        registration_obj = self.env['event.registration']
        partner_obj = self.env['res.partner']
        print self.env.context.get('active_ids', [])
        for partner_id in self.env.context.get('active_ids', []):
            partner = partner_obj.browse(partner_id)
            registration_obj.create(self._prepare_registration(partner))
