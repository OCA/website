# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from psycopg2 import IntegrityError

from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase


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
        self.ab = self.wsr.create({
            "origin": "/a",
            "destination": "/b",
        })
        self.cd = self.wsr.create({
            "origin": "/c",
            "destination": "/d",
        })
        self.de = self.wsr.create({
            "origin": "/d",
            "destination": "/e",
        })
        self.fa = self.wsr.create({
            "origin": "/f",
            "destination": "/a",
        })

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
        with self.assertRaises(IntegrityError):
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

    def test_no_recursive_first(self):
        """Recursive redirections are forbidden."""
        with self.assertRaises(ValidationError):
            self.wsr.create({
                "origin": "/e",
                "destination": "/c",
            })

    def test_smart_add_modify_by_origin(self):
        """:meth:`~.smart_add` replaces destination when origin is the same."""
        self.wsr.smart_add("/a", "/c")
        self.assertEqual(self.ab.origin, "/a")
        self.assertEqual(self.ab.destination, "/c")
        self.assertEqual(self.cd.origin, "/c")
        self.assertEqual(self.cd.destination, "/d")
        self.assertEqual(self.de.origin, "/d")
        self.assertEqual(self.de.destination, "/e")
        self.assertEqual(self.fa.origin, "/f")
        self.assertEqual(self.fa.destination, "/c")

    def test_smart_add_modify_by_destination(self):
        """:meth:`~.smart_add` replaces destination when it is the same."""
        self.wsr.smart_add("/d", "/e")
        self.assertEqual(self.ab.origin, "/a")
        self.assertEqual(self.ab.destination, "/b")
        self.assertEqual(self.cd.origin, "/c")
        self.assertEqual(self.cd.destination, "/e")
        self.assertEqual(self.de.origin, "/d")
        self.assertEqual(self.de.destination, "/e")
        self.assertEqual(self.fa.origin, "/f")
        self.assertEqual(self.fa.destination, "/a")

    def test_smart_add_unlink_recursive(self):
        """:meth:`~.smart_add` unlinks redirection when it is recursive."""
        self.wsr.smart_add("/d", "/c")
        self.assertEqual(self.ab.origin, "/a")
        self.assertEqual(self.ab.destination, "/b")
        self.assertFalse(self.cd.exists())
        self.assertEqual(self.de.origin, "/d")
        self.assertEqual(self.de.destination, "/c")
        self.assertEqual(self.fa.origin, "/f")
        self.assertEqual(self.fa.destination, "/a")

    def test_smart_add_create(self):
        """:meth:`~.smart_add` creates a redirection."""
        self.wsr.smart_add("/g", "/h")
        self.assertEqual(self.ab.origin, "/a")
        self.assertEqual(self.ab.destination, "/b")
        self.assertEqual(self.cd.origin, "/c")
        self.assertEqual(self.cd.destination, "/d")
        self.assertEqual(self.de.origin, "/d")
        self.assertEqual(self.de.destination, "/e")
        self.assertEqual(self.fa.origin, "/f")
        self.assertEqual(self.fa.destination, "/a")
        self.assertTrue(self.wsr.search([
            ("origin", "=", "/g"),
            ("destination", "=", "/h"),
        ]))
