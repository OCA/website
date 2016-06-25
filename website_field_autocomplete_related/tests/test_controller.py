# -*- coding: utf-8 -*-
# © 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import mock
from contextlib import contextmanager

from openerp.tests.common import TransactionCase

from openerp.addons.website_field_autocomplete_related.controllers import main


class TestController(TransactionCase):

    def setUp(self):
        super(TestController, self).setUp()
        self.Controller = main.WebsiteAutocomplete
        self.controller = self.Controller()
        self.record = self.env.user
        self.fields = [
            'name', 'partner_id.name',
        ]

    @contextmanager
    def mock_controller(self):
        with mock.patch.object(main.Website, '_get_autocomplete_data') as mk:
            with mock.patch.object(main, 'request') as request:
                request.env[''].search.return_value = self.record
                mk.return_value = {
                    self.record.id: {
                        'name': self.record.name,
                    }
                }
                yield {
                    'super': mk,
                    'request': request,
                }

    def test_get_autocomplete_data_search(self):
        """ It should call search w/ proper domain """
        expect = [('name', '=', self.record.name)]
        with self.mock_controller() as mk:
            self.controller._get_autocomplete_data(
                self.record._name, expect, self.fields, 10
            )
            mk['request'].env[''].search.assert_called_once_with(
                expect
            )

    def test_get_autocomplete_data_return(self):
        """ It should return dictionary w/ proper vals """
        with self.mock_controller():
            res = self.controller._get_autocomplete_data(
                self.record._name, [], self.fields, 10
            )
            expect = {
                self.record.id: {
                    'name': self.record.name,
                    'partner_id.name': self.record.partner_id.name,
                },
            }
            self.assertDictEqual(expect, res)

    def test_get_relational_data(self):
        """ It should return proper field value """
        with self.mock_controller():
            res = self.controller._get_relation_data(
                self.record, self.fields[1],
            )
            self.assertEqual(
                self.record.partner_id.name,
                res,
            )
