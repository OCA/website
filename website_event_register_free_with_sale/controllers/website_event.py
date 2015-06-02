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
from openerp import http
from openerp.http import request
from openerp.addons.website_event_sale.controllers.main import website_event


class WebsiteEvent(website_event):
    @http.route(['/event/cart/update'], type='http', auth="public",
                methods=['POST'], website=True)
    def cart_update(self, **post):
        has_paid_tickets = False
        post['free_tickets'] = 0
        for key, value in post.items():
            qty = int(value or "0")
            ticket_words = key.split("-")
            ticket_id = (ticket_words[0] == 'ticket' and
                         int(ticket_words[1]) or None)
            if not qty or not ticket_id:
                continue
            ticket = request.env['event.event.ticket'].sudo().browse(ticket_id)
            if not ticket.price:
                # Accumulate possible multiple free tickets
                post['free_tickets'] = (
                    str(int(post['free_tickets']) + qty))
            else:
                has_paid_tickets = True
                # Add to shopping cart the rest of the items
                order = request.website.sale_get_order(force_create=1)
                order.with_context(event_ticket_id=ticket.id)._cart_update(
                    product_id=ticket.product_id.id, add_qty=qty)
        if not post['free_tickets'] and not has_paid_tickets:
            return request.redirect("/event/%s" % post['event_id'])
        request.session.update({
            'free_tickets': post['free_tickets'],
            'event_id': post['event_id'],
        })
        return request.redirect("/shop/checkout")
