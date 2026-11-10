# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import html

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestCookieFirstTracking(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("base.default_website")
        cls.website.write(
            {
                "sequence": -100,
                "domain": cls.base_url(),
                "cookiefirst_identifier": "test-cookie-first",
                "cookies_bar": False,
            }
        )

    def _render_tracking(self, key):
        self.website.google_analytics_key = key
        # Fetch HTML only: no browser executes Google or CookieFirst scripts.
        response = self.url_open("/legal/cookies-policy")
        self.assertEqual(response.status_code, 200)
        return html.fromstring(response.content)

    def test_cookiefirst_controls_analytics_and_tag_manager(self):
        for key in ("G-TEST123", "GTM-TEST123"):
            with self.subTest(key=key):
                document = self._render_tracking(key)
                consent = document.xpath("//head/script[@id='cookiefirst_consent']")
                self.assertEqual(len(consent), 1)
                self.assertIn("test-cookie-first/consent.js", consent[0].get("src"))
                tracking = document.xpath("//script[@id='tracking_code']")
                self.assertEqual(len(tracking), 1)
                scripts = tracking
                if key.startswith("G-"):
                    scripts += tracking[0].xpath("following-sibling::script[1]")
                    self.assertEqual(len(scripts), 2)
                for script in scripts:
                    self.assertEqual(script.get("type"), "text/plain")
                    self.assertEqual(
                        script.get("data-cookiefirst-category"), "performance"
                    )
                head_scripts = document.xpath("//head//script")
                self.assertLess(
                    head_scripts.index(consent[0]), head_scripts.index(tracking[0])
                )
                config = document.xpath(
                    "//script[@id='cookiefirst_tracking_code_config']"
                )
                self.assertEqual(len(config), 1)
                self.assertIn("window.dataLayer", config[0].text)
                self.assertIn("function gtag()", config[0].text)
                self.assertLess(
                    head_scripts.index(consent[0]), head_scripts.index(config[0])
                )
                self.assertFalse(document.xpath("//script[@id='tracking_code_config']"))
                rendered = html.tostring(document, encoding="unicode")
                self.assertNotIn("updateConsents", rendered)
                self.assertNotIn("optionalCookiesAccepted", rendered)
                self.assertNotIn("optionalCookiesDenied", rendered)

    def test_native_tracking_without_cookiefirst(self):
        self.website.cookiefirst_identifier = False
        self._assert_native_tracking()

    def test_native_tracking_without_domain(self):
        self.website.domain = False
        self._assert_native_tracking()

    def test_cookiefirst_without_google_tracking(self):
        document = self._render_tracking(False)
        self.assertEqual(
            len(document.xpath("//head/script[@id='cookiefirst_consent']")), 1
        )
        self.assertFalse(document.xpath("//script[@id='tracking_code']"))

    def _assert_native_tracking(self):
        for key in ("G-TEST123", "GTM-TEST123"):
            with self.subTest(key=key):
                document = self._render_tracking(key)
                self.assertFalse(document.xpath("//script[@id='cookiefirst_consent']"))
                tracking = document.xpath("//script[@id='tracking_code']")
                self.assertEqual(len(tracking), 1)
                scripts = tracking + tracking[0].xpath("following-sibling::script[1]")
                for script in scripts:
                    self.assertNotEqual(script.get("type"), "text/plain")
                    self.assertIsNone(script.get("data-cookiefirst-category"))
                config = document.xpath("//script[@id='tracking_code_config']")
                self.assertEqual(len(config), 1)
                self.assertIn('updateConsents("granted")', config[0].text_content())
                self.assertIn("optionalCookiesAccepted", config[0].text_content())
                self.assertIn("optionalCookiesDenied", config[0].text_content())
