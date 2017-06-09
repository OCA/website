# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License APL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase


class TestController(HttpCase):

    def test_legal(self):
        """ It should return a 200 for the default page. """
        response = self.url_open('/legal')
        self.assertEqual(
            response.getcode(),
            200,
        )

    def test_unknown(self):
        """ It should return a 404 for unknown pages. """
        response = self.url_open('/legal/no-page')
        self.assertEqual(
            response.getcode(),
            404,
        )

    def test_privacy(self):
        """ It should return a 200 for a defined page. """
        response = self.url_open('/legal/privacy')
        self.assertEqual(
            response.getcode(),
            200,
        )
