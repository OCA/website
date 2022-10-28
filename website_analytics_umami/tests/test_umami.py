# Copyright 2022 Yiğit Budak (https://github.com/yibudak)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
import odoo.tests


@odoo.tests.common.tagged("post_install")
class TestUmamiAnalytics(odoo.tests.HttpCase):
    def setUp(self):
        super(TestUmamiAnalytics, self).setUp()
        self.domain = "http://" + odoo.tests.HOST
        self.website = self.env["website"].create(
            {
                "name": "test base url",
                "domain": self.domain,
                "has_umami_analytics": True,
                "umami_script_name": "umami.js",
                "umami_analytics_host": "odoo.local",
            }
        )
        self.test__get_umami_script_url()

    def test__get_umami_script_url(self):
        url = self.website._get_umami_script_url()
        self.assertEqual(url, "https://odoo.local/umami.js")
