# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from json import dumps
from datetime import datetime

from openerp import http


class WebsiteCalendarSnippet(http.Controller):

    @http.route(
        ['/calendar_snippet/get_events/<int:start>/<int:end>'],
        type='http',
        auth='public',
        website=True)
    def get_events(self, start, end, **post):
        request = http.request

        # Get events
        calendar_event_obj = request.env['calendar.event']
        calendar_events = calendar_event_obj.search(
            [('start', '<', unicode(datetime.fromtimestamp(end))),
             ('stop', '>', unicode(datetime.fromtimestamp(start)))]
        )

        contacts = []
        if request.website.user_id.id != request.env.uid:
            calendar_contact_obj = request.env['calendar.contacts']
            calendar_contacts = calendar_contact_obj.search(
                [('user_id', '=', request.env.uid)]
            )

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

        return dumps({'events': events, 'contacts': contacts})
