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
from openerp import http, fields
from openerp.addons.website_event.controllers.main import website_event


class WebsiteEvent(website_event):
    @http.route(['/event/<model("event.event"):event>/register/register_free'],
                type='http', auth="public", website=True)
    def event_register_free(self, event, **post):
        def validate(name, force_check=False):
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
        # if logged in, use that info
        if http.request.env.ref('base.public_user') != http.request.env.user\
                and validate('tickets', True):
            registration = http.request.env['event.registration']\
                .sudo()\
                .create({
                    'origin': 'Website',
                    'nb_register': int(post['tickets']),
                    'event_id': event.id,
                    'partner_id': http.request.env.user.partner_id.id,
                    'date_open': fields.Datetime.now(),
                    'user_id': http.request.env.user.id,
                })
            registration._onchange_partner()
            registration.registration_open()
            return http.request.render(
                'website_event_register_free.partner_register_confirm',
                {'registration': registration})
        # othrwise, create a simple registration
        if all(map(lambda f: validate(f, True), ['name', 'email', 'tickets'])):
            registration = http.request.env['event.registration']\
                .sudo()\
                .create({
                    'origin': 'Website',
                    'nb_register': int(post['tickets']),
                    'event_id': event.id,
                    'date_open': fields.Datetime.now(),
                    'email': post['email'],
                    'phone': post['phone'],
                    'name': post['name'],
                })
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
