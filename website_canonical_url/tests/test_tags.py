# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase
from lxml.html import document_fromstring


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        self.root = 'http://' + self.xmlrpc_db._ServerProxy__host
        self.url = "/page/website_canonical_url.canonical_demo"
        self.url_absolute = self.root + "/.." + self.url
        self.get = "?ultimate_answer=42"
        self.url_get = "%s%s" % (self.url, self.get)
        self.url_data = self.url_open(self.url_get)
        self.doc = document_fromstring(self.url_data.read())

    def test_canonical(self):
        """Canonical URL is built OK."""
        node = self.doc.xpath("/html/head/link[@rel='canonical']")[0]
        self.assertEqual(node.attrib["href"], self.url_absolute)

    def test_pager_next(self):
        """Next pager link is OK."""
        node = self.doc.xpath("/html/head/link[@rel='next']")[0]
        self.assertEqual(
            node.attrib["href"],
            "%s/page/3%s" % (self.url, self.get),
        )

    def test_pager_prev(self):
        """Prev pager link is OK."""
        node = self.doc.xpath("/html/head/link[@rel='prev']")[0]
        self.assertEqual(node.attrib["href"], self.url_get)
