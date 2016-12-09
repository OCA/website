# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class WebsiteSeoRedirectionCase(TransactionCase):
    def setUp(self):
        super(WebsiteSeoRedirectionCase, self).setUp()
        self.wsr = self.env["website.seo.redirection"]
        self.bad_inputs = {
            "http://example.com/test",
            "test",
            "/test?db=test",
            "/test&other",
            "/test#anchor",
        }

    def test_bad_origin(self):
        """Cannot enter a malformed origin URL."""
        for sample in self.bad_inputs:
            with self.assertRaises(ValidationError):
                with self.env.cr.savepoint():
                    self.wsr.create({
                        "origin": sample,
                        "destination": "/good-url",
                    })

    def test_bad_redirection(self):
        """Cannot enter a malformed redirection URL."""
        for sample in self.bad_inputs:
            with self.assertRaises(ValidationError):
                with self.env.cr.savepoint():
                    self.wsr.create({
                        "origin": "/good-url",
                        "destination": sample,
                    })

    def test_equal_origin_redirection(self):
        """Cannot create a redirection to itself."""
        with self.assertRaises(ValidationError):
            self.wsr.create({
                "origin": "/same-url",
                "destination": "/same-url",
            })

    def test_find_origin(self):
        """The right origin is found."""
        record = self.wsr.create({
            "origin": "/page/example-page",
            "destination": "/example",
        })
        # Search by redirection, return origin
        self.assertEqual(
            self.wsr.find_origin(record.destination),
            record.origin)

        # Search by origin, return itself
        self.assertEqual(record.origin, record.origin)

        # Search by whatever, return itself
        self.assertEqual("/page/whatever", "/page/whatever")
