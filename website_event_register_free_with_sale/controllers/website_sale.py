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
from openerp.http import request, route
from openerp.addons.website_sale.controllers.main import website_sale

from ..exceptions import NoNeedForSOError


class WebsiteSale(website_sale):
    mandatory_free_registration_fields = ["name", "phone", "email"]
    optional_free_registration_fields = ["street", "city", "country_id", "zip"]

    def _get_mandatory_billing_fields(self):
        if self._only_free_ticket_checkout():
            return self.mandatory_free_registration_fields
        else:
            return super(WebsiteSale, self)._get_mandatory_billing_fields()

    def _get_optional_billing_fields(self):
        if self._only_free_ticket_checkout():
            return self.optional_free_registration_fields
        else:
            return super(WebsiteSale, self)._get_optional_billing_fields()

    def _only_free_ticket_checkout(self):
        """Check if we are checking out only free tickets."""
        has_free = request.session.get("free_tickets")
        order = request.website.sale_get_order(force_create=0)
        has_paid = order and order.order_line
        return has_free and not has_paid

    def _register_event_free(self, post):
        """Register current visitor in a free event.

        :param dict post:
            Used keys:

            - name
            - email
            - phone

        :raise KeyError:
            When ``free_tickets`` or ``event_id`` are not found under
            :class:`~request.session`, or are empty.

        :raise NoNeedForSOError:
            When there is nothing left to buy after free registrations are
            processed. Includes the registration inside exception's
            ``registration`` attribute.

        :return openerp.Model:
            Registration that has been created.
        """
        tickets = request.session["free_tickets"]
        event = request.env["event.event"].browse(request.session["event_id"])
        if not (tickets and event):
            raise KeyError
        Registration = request.env['event.registration']
        registration_vals = Registration._prepare_registration(
            event,
            dict(post, tickets=tickets),
            request.uid,
            partner=(request.env.user != request.website.user_id and
                     request.env.user.partner_id),
        )
        registration = Registration.sudo().create(registration_vals)
        if registration.partner_id:
            registration._onchange_partner()
        registration.registration_open()
        try:
            if self._only_free_ticket_checkout():
                raise NoNeedForSOError(registration)
        finally:
            del request.session["free_tickets"], request.session["event_id"]
        request.session["free_registration_id"] = registration.id
        return registration

    def checkout_form_save(self, checkout):
        """Save free registrations too."""
        try:
            self._register_event_free(
                self.checkout_parse("billing", checkout, True))
        except KeyError:
            pass
        return super(WebsiteSale, self).checkout_form_save(checkout)

    @route()
    def confirm_order(self, **post):
        """Skip SO creation & payment for only-free events."""
        try:
            return super(WebsiteSale, self).confirm_order(**post)
        except NoNeedForSOError as ex:
            return request.render(
                'website_event_register_free.partner_register_confirm',
                {'registration': ex.registration})

    @route()
    def payment(self, **post):
        """Add free registration confirmation to page."""
        result = super(WebsiteSale, self).payment(**post)
        registration = request.session.pop("free_registration_id", None)
        if registration:
            result.qcontext["free_registration"] = \
                request.env["event.registration"].browse(registration)
        return result
