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
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website_event_register_free.controllers.website_event \
    import WebsiteEvent


class WebsiteSale(website_sale):
    mandatory_free_registration_fields = ["name", "phone", "email"]
    # TODO: Not used yet
    optional_free_registration_fields = ["street", "city", "country_id", "zip"]

    def checkout_form_validate_free(self, data):
        errors = dict()
        if request.session.get('free_tickets'):
            # Make validation for free tickets
            for field_name in self.mandatory_free_registration_fields:
                if not data.get(field_name, '').strip():
                    errors[field_name] = 'missing'
                elif not WebsiteEvent()._validate(field_name, data, True):
                    # Patch for current free registration implementation
                    errors[field_name] = 'error'
        return errors

    @http.route(['/shop/checkout'], type='http', auth="public", website=True)
    def checkout(self, **post):
        order = request.website.sale_get_order(force_create=0)
        has_paid_tickets = bool(order.order_line)
        if request.session.get('free_tickets') and not has_paid_tickets:
            values = self.checkout_values(data={'shipping_id': -1})
            return request.website.render("website_sale.checkout", values)
        else:
            return super(WebsiteSale, self).checkout(**post)

    @http.route(['/shop/confirm_order'], type='http', auth="public",
                website=True)
    def confirm_order(self, **post):
        if (request.session.get('free_tickets') is None and
                request.session.get('has_paid_tickets') is None):
            # Handle call of this method from regular shop
            return super(WebsiteSale, self).confirm_order(**post)
        if request.session.get('free_tickets'):
            values = self.checkout_values(post)
            values['error'] = self.checkout_form_validate_free(post)
            if values["error"]:
                return request.website.render("website_sale.checkout", values)
            post['tickets'] = request.session['free_tickets']
            event = request.env['event.event'].browse(
                int(request.session['event_id']))
            if (http.request.env.ref('base.public_user') !=
                    http.request.env.user):
                partner = http.request.env.user.partner_id
            else:
                partner = False
            # Use same hook as without website_sale
            reg_obj = http.request.env['event.registration']
            registration_vals = reg_obj._prepare_registration(
                event, post, http.request.env.user.id, partner=partner)
            registration = reg_obj.sudo().create(registration_vals)
            if registration.partner_id:
                registration._onchange_partner()
            registration.registration_open()
        order = request.website.sale_get_order(force_create=0)
        has_paid_tickets = bool(order.order_line)
        if has_paid_tickets:
            return super(WebsiteSale, self).confirm_order(**post)
        elif request.session.get('free_tickets'):
            request.session['free_tickets'] = 0
            return http.request.render(
                'website_event_register_free.partner_register_confirm',
                {'registration': registration})
        else:
            return http.request.redirect('/event')
