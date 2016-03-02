# -*- coding: utf-8 -*-
# © 2016 ONESTEiN BV (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
from datetime import datetime

from openerp import http
from openerp.http import request


class WebsiteCalendarBlock(http.Controller):

    @http.route(
        ['/calendar_block/get_events/<int:start>/<int:end>'],
        type='http',
        auth='public',
        website=True)
    def get_events(self, start, end, **post):
        cr, uid, context = request.cr, request.uid, request.context

        # Get events
        calendar_event_obj = request.registry['calendar.event']
        calendar_event_ids = calendar_event_obj.search(
            cr, uid, [('start', '<', unicode(datetime.fromtimestamp(end))),
                      ('stop', '>', unicode(datetime.fromtimestamp(start)))],
            context=context)
        calendar_events = calendar_event_obj.browse(
            cr, uid, calendar_event_ids, context=context)

        contacts = []
        if request.website.user_id.id != uid:
            calendar_contact_obj = request.registry['calendar.contacts']
            calendar_contact_ids = calendar_contact_obj.search(
                cr, uid, [('user_id', '=', uid)], context=context)
            calendar_contacts = calendar_contact_obj.browse(
                cr, uid, calendar_contact_ids, context=context)

            # Create response (Cannot serialize object)
            contacts.append(request.env.user.partner_id.id)
            for contact in calendar_contacts:
                contacts.append(contact.partner_id.id)

        # Events
        events = []
        for calendar_event in calendar_events:
            # Fetch attendees
            attendees = []
            for attendee_id in calendar_event.attendee_ids:
                attendees.append({'id': attendee_id.partner_id.id,
                                  'name': attendee_id.partner_id.name})

            events.append(
                {'id': calendar_event.id,
                 'start': calendar_event.start,
                 'end': calendar_event.stop,
                 'title': calendar_event.name,
                 'allDay': calendar_event.allday,
                 'color': calendar_event.color_partner_id,
                 'attendees': attendees
                 })

        return json.dumps({'events': events, 'contacts': contacts})
