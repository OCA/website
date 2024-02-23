# Copyright 2023 Onestein (<https://www.onestein.eu>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from lxml import html

from odoo.tests import common, tagged


@tagged("-at_install", "post_install")
class TestWebsiteAnalyticsMatomo(common.HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env.ref("website.default_website")
        self.base_view = self.env["ir.ui.view"].create(
            {
                "name": "Base",
                "type": "qweb",
                "arch": """<t name="Homepage" t-name="website.base_view">
                        <t t-call="website.layout">
                            I am a generic page
                        </t>
                    </t>""",
                "key": "test.base_view",
            }
        )
        self.page = self.env["website.page"].create(
            {
                "view_id": self.base_view.id,
                "url": "/page_1",
                "is_published": True,
                "website_id": self.website.id,
            }
        )

    def test_01_defaults(self):
        """Check default values"""
        self.assertFalse(self.website.has_matomo_analytics)
        self.assertEqual(self.website.matomo_analytics_id, "1")
        self.assertFalse(self.website.matomo_analytics_host)
        self.assertFalse(self.website.matomo_analytics_host_url)
        self.assertFalse(self.website.matomo_enable_heartbeat)
        self.assertEqual(self.website.matomo_heartbeat_timer, 15)
        self.assertFalse(self.website.matomo_enable_userid)
        self.assertFalse(self.website.matomo_get_userid)

    def test_02_compute_matomo_analytics_host_url(self):
        """Computation of field matomo_analytics_host_url"""
        self.website.has_matomo_analytics = True
        self.assertEqual(self.website.matomo_analytics_host_url, "")

        self.website.matomo_analytics_host = "matomo.example.host"
        self.assertIn("https://", self.website.matomo_analytics_host_url)
        self.assertIn("matomo.example.host", self.website.matomo_analytics_host_url)

        self.website.matomo_analytics_host = "http://matomo.example.host"
        self.assertIn("http://", self.website.matomo_analytics_host_url)
        self.assertIn("matomo.example.host", self.website.matomo_analytics_host_url)

        self.website.matomo_analytics_host = ""
        self.assertEqual(self.website.matomo_analytics_host_url, "")

    def test_03_compute_matomo_userid(self):
        """Computation of field matomo_get_userid"""
        self.website.has_matomo_analytics = True
        self.website.matomo_analytics_host = "matomo.example.host"
        self.assertEqual(self.website.matomo_get_userid, "")

        self.website.matomo_enable_userid = True
        self.assertTrue(self.website.matomo_get_userid)
        self.assertEqual(self.website.matomo_get_userid, str(self.env.user.id))
        self.assertNotEqual(self.website.matomo_get_userid, self.website.user_id.login)

        self.website.matomo_analytics_host = ""
        self.assertEqual(self.website.matomo_get_userid, "")

    def test_04_tracker_script_in_page(self):
        """Check matomo tracker script in the page"""

        # matomo tracker script not in the page
        self.authenticate("admin", "admin")
        r = self.url_open(self.page.url)
        self.assertEqual(r.status_code, 200)
        root_html = html.fromstring(r.content)
        tracking_script = root_html.xpath('//script[@id="matomo_analytics"]')
        self.assertFalse(tracking_script)

        # enable analytics tracker
        self.website.has_matomo_analytics = True
        self.website.matomo_analytics_host = "matomo.example.host"

        # matomo tracker script present in the page
        self.authenticate("admin", "admin")
        r = self.url_open(self.page.url)
        self.assertEqual(r.status_code, 200)
        root_html = html.fromstring(r.content)
        tracking_script = root_html.xpath('//script[@id="matomo_analytics"]')[0]
        self.assertIn("trackPageView", tracking_script.text)
        self.assertIn("enableLinkTracking", tracking_script.text)
        self.assertIn("setSiteId", tracking_script.text)
        self.assertNotIn("setUserId", tracking_script.text)

        # enable User ID feature
        self.website.matomo_enable_userid = True

        # Tracking User ID enabled in the page
        r = self.url_open(self.page.url)
        self.assertEqual(r.status_code, 200)
        root_html = html.fromstring(r.content)
        tracking_script = root_html.xpath('//script[@id="matomo_analytics"]')[0]
        self.assertIn("setUserId", tracking_script.text)
