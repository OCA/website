# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
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
from openerp import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    def _prepare_registration(self, event_id, post, user_id, partner=False):
        return {
            'origin': 'Website',
            'nb_register': int(post['tickets']),
            'event_id': event_id,
            'date_open': fields.Datetime.now(),
            'email': post.get('email') or partner and partner.email,
            'phone': post.get('phone') or partner and partner.phone,
            'name': post.get('name') or partner and partner.name,
            'user_id': user_id,
            'partner_id': partner and partner.id,
        }
