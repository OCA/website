# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
from openerp.addons.website_event.controllers.main import website_event


class WebsiteEvent(website_event):
    def _validate(self, name, post, force_check=False):
        if name in post or force_check:
            if name == 'name' and not post.get('name', '').strip():
                return False
            if name == 'email' and not post.get('email', '').strip():
                return False
            if name == 'tickets' and (
                    not post.get('tickets', '').isdigit() or
                    int(post.get('tickets')) <= 0):
                return False
        return True

    @http.route(['/event/<model("event.event"):event>/register/register_free'],
                type='http', auth="public", website=True)
    def event_register_free(self, event, **post):
        def validate(name, force_check=False):
            return self._validate(name, post, force_check=force_check)

        reg_obj = http.request.env['event.registration']
        registration_vals = {}
        if (http.request.env.ref('base.public_user') !=
                http.request.env.user and
                validate('tickets', force_check=True)):
            # if logged in, use that info
            registration_vals = reg_obj._prepare_registration(
                event.id, post, http.request.env.user.id,
                partner=http.request.env.user.partner_id)
        if all(map(lambda f: validate(f, force_check=True),
                   ['name', 'email', 'tickets'])):
            # otherwise, create a simple registration
            registration_vals = reg_obj._prepare_registration(
                event.id, post, http.request.env.user.id)
        if registration_vals:
            registration = reg_obj.sudo().create(registration_vals)
            if registration.partner_id:
                registration._onchange_partner()
            registration.registration_open()
            return http.request.render(
                'website_event_register_free.partner_register_confirm',
                {'registration': registration})
        values = {
            'event': event,
            'range': range,
            'tickets': post.get('tickets', 1),
            'validate': validate,
            'post': post,
        }
        return http.request.render(
            'website_event_register_free.partner_register_form', values)
