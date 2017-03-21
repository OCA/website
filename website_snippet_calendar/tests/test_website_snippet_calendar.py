# -*- coding: utf-8 -*-
# Copyright 2017 Onestein (<http://www.onestein.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from json import loads
from time import mktime
from mock import patch

from openerp.tests.common import TransactionCase
from openerp import http
from openerp.fields import Datetime
from ..controllers.main import WebsiteCalendarSnippet

class TestWebsiteSnippetCalendar(TransactionCase):
    def test_controller(self):
        select_start = '2017-03-01 11:00:00'
        select_stop = '2017-03-01 14:00:00'
        event_obj = self.env['calendar.event']
        event_obj.create({
            'name': 'Test',
            'start': '2017-03-01 12:00:00',
            'stop': '2017-03-01 13:00:00'
        })
        events = event_obj.search([('start', '<', select_stop),
                                   ('stop', '>', select_start)])

        select_start_obj = Datetime.from_string(select_start)
        select_stop_obj = Datetime.from_string(select_stop)
        select_start_ts = mktime(select_start_obj.timetuple())
        select_stop_ts = mktime(select_stop_obj.timetuple())

        with patch.object(http, 'request') as request:
            request.env = self.env
            controller = WebsiteCalendarSnippet()
            res_str = controller.get_events(
                select_start_ts,
                select_stop_ts).data
            res = loads(res_str)
            self.assertListEqual(map(lambda e: e['id'], res['events']),
                                 events.ids)
