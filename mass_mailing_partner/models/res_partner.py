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
