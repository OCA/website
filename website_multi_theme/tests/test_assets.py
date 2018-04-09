# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from lxml import html
from odoo.tests.common import PORT, HttpCase


class UICase(HttpCase):

    def test_localhost(self):
        """Check localhost downloads its multiwebsite-enabled assets."""
        response = self.url_open("http://localhost:%d" % PORT, timeout=60)
        self.assertEqual(response.status_code, 200)
        result = html.document_fromstring(response.content)
        self.assertFalse(result.xpath(
            "//head/link[contains(@href, 'web.assets_frontend')]"))
        self.assertTrue(result.xpath(
            """//head/link[contains(@href,
               'website_multi_theme.auto_assets_website')]"""))

    def test_0_0_0_0(self):
        """Check 0.0.0.0 downloads its default assets."""
        response = self.url_open("http://0.0.0.0:%d" % PORT, timeout=60)
        self.assertEqual(response.status_code, 200)
        result = html.document_fromstring(response.content)
        self.assertFalse(result.xpath(
            "//head/link[contains(@href, 'web.assets_frontend')]"))
        self.assertTrue(result.xpath(
            """//head/link[contains(@href,
               'website_multi_theme.auto_assets_website')]"""))
