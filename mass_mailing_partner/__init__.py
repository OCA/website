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
from . import models
from openerp import SUPERUSER_ID


def _match_existing_contacts(cr, registry):
    contact_model = registry['mail.mass_mailing.contact']
    partner_model = registry['res.partner']
    contact_ids = contact_model.search(cr, SUPERUSER_ID, [])
    for contact in contact_model.browse(cr, SUPERUSER_ID, contact_ids):
        if contact.email:
            partner_ids = partner_model.search(
                cr, SUPERUSER_ID, [('email', '=ilike', contact.email)])
            if not partner_ids:
                contact_vals = contact_model.read(cr, SUPERUSER_ID, contact.id)
                vals = contact_model._prepare_partner(contact_vals)
                partner_id = partner_model.create(cr, SUPERUSER_ID, vals)
            else:
                partner_id = partner_ids[0]
                partner_model.write(cr, SUPERUSER_ID, partner_id,
                                    {'opt_out': contact.opt_out})
            contact_model.write(cr, SUPERUSER_ID, contact.id,
                                {'partner_id': partner_id})
