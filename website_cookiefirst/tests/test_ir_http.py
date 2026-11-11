# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from urllib.parse import quote

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestOptionalCookies(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].get_current_website()
        self.website.write(
            {"cookiefirst_identifier": "1234567890", "cookies_bar": False}
        )

    def _utm_cookie(self, consent=None):
        self.opener.cookies.clear()
        if consent is not None:
            self.opener.cookies.set(
                "cookiefirst-consent", quote(json.dumps(consent)), domain="127.0.0.1"
            )
        response = self.url_open("/?utm_source=newsletter")
        self.assertEqual(response.status_code, 200)
        return self.opener.cookies.get("odoo_utm_source")

    def test_no_choice(self):
        self.assertFalse(self._utm_cookie())

    def test_rejected(self):
        self.assertFalse(self._utm_cookie({"necessary": True, "performance": False}))

    def test_accepted(self):
        self.assertEqual(
            self._utm_cookie({"necessary": True, "performance": True}), "newsletter"
        )

    def test_malformed(self):
        self.opener.cookies.clear()
        self.opener.cookies.set("cookiefirst-consent", "not-json", domain="127.0.0.1")
        self.url_open("/?utm_source=newsletter")
        self.assertFalse(self.opener.cookies.get("odoo_utm_source"))

    def test_without_cookiefirst(self):
        self.website.cookiefirst_identifier = False
        self.assertEqual(self._utm_cookie(), "newsletter")
