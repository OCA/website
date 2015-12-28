# -*- coding: utf-8 -*-
# (c) 2015 Incaser Informatica S.L. - Sergio Teruel
# (c) 2015 Incaser Informatica S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.tools.translate import _

from openerp.addons.website_event.controllers.main import website_event


class WebsiteEventOrganizer(website_event):

    @http.route(
        ['/event', '/event/page/<int:page>'],
        type='http', auth="public", website=True)
    def events(self, page=1, **searches):
        response = super(WebsiteEventOrganizer, self).events(page, **searches)
        current_organizer = None

        searches.update(response.qcontext['searches'])
        searches.setdefault('organizer', 'all')

        event_obj = request.env['event.event']
        events = response.qcontext['event_ids']

        organizers = event_obj.read_group(
            [('id', 'in', events.ids)], ['organizer_id'], 'organizer_id')
        organizers.insert(0, {
            'organizer_id_count': len(events),
            'organizer_id': ("all", _("All Organizers"))
        })

        if searches['organizer'] != 'all':
            events = events.filtered(
                lambda x: x.organizer_id.id == int(searches["organizer"]))
            current_organizer = \
                events and events[0].sudo().organizer_id.name or ''

        step = 10  # events per page
        pager = request.website.pager(
            url="/event",
            url_args={
                'date': searches.get('date'),
                'type': searches.get('type'),
                'country': searches.get('country'),
                'organizer': searches.get('organizer'),
            },
            total=len(events),
            page=page,
            step=step,
            scope=5)
        offset = response.qcontext['pager']['offset']
        events = events[offset:offset+step]

        response.qcontext.update({
            'current_organizer': current_organizer,
            'organizers': organizers,
            'event_ids': events,
            'searches': searches,
            'pager': pager,
        })
        return response
