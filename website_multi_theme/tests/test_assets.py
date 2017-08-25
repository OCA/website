# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from lxml import html
from odoo.tests.common import PORT, HttpCase


class UICase(HttpCase):
    def setUp(self):
        super(UICase, self).setUp()
        with self.cursor() as cr:
            env = self.env(cr)
            localhost = env.ref("website.default_website")
            localhost.write({
                "domain": "localhost",
                "multi_theme_id": env.ref("website_multi_theme.demo_multi").id,
            })
            # Create a 127.0.0.1 host, different to localhost
            ip = env["website"].create({
                "name": "127.0.0.1",
                "domain": "127.0.0.1",
                "multi_theme_id": False,
            })
            # Copy the demo page in 127.0.0.1
            page = env.ref("website_multi_theme.demo_page")
            page.website_id = localhost
            page.copy({
                "website_id": ip.id,
            })

    def test_localhost(self):
        """Check localhost downloads its multiwebsite-enabled assets."""
        response = self.url_open("http://localhost:%d" % PORT)
        self.assertEqual(response.getcode(), 200)
        result = html.document_fromstring(response.read())
        self.assertFalse(result.xpath(
            "//head/link[contains(@href, 'web.assets_frontend')]"))
        self.assertTrue(result.xpath(
            """//head/link[contains(@href,
               'website_multi_theme.auto_assets_website')]"""))

    def test_127_0_0_1(self):
        """Check 127.0.0.1 downloads its default assets."""
        response = self.url_open("http://127.0.0.1:%d" % PORT)
        self.assertEqual(response.getcode(), 200)
        result = html.document_fromstring(response.read())
        self.assertTrue(result.xpath(
            "//head/link[contains(@href, 'web.assets_frontend')]"))
        self.assertFalse(result.xpath(
            """//head/link[contains(@href,
               'website_multi_theme.auto_assets_website')]"""))
