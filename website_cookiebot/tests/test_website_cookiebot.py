# © 2024 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo.tests.common import TransactionCase


class TestWebsiteCookiebot(TransactionCase):
    def test_conf_cookiebot_domain(self):
        domain_group_id = "9a9999a9-aa99-9a99-999a-aa999999999a"
        config = self.env["res.config.settings"].sudo().create({})
        config.write({"cookiebot_dgid": domain_group_id})
        self.assertTrue(config.cookiebot_enabled)
        self.assertFalse(config.website_cookies_bar)
        self.assertEqual(config.cookiebot_dgid, domain_group_id)

    def test_conf_website_cookies_bar(self):
        config = self.env["res.config.settings"].sudo().create({})
        config.write({"website_cookies_bar": True})
        config._onchange_website_cookies_bar()
        self.assertTrue(config.website_cookies_bar)
        self.assertFalse(config.cookiebot_enabled)
        self.assertFalse(config.cookiebot_dgid)

    def test_conf_cookies_enabled(self):
        config = self.env["res.config.settings"].sudo().create({})
        config.write({"cookiebot_enabled": True})
        config._onchange_cookiebot_enabled()
        self.assertFalse(config.website_cookies_bar)
        self.assertTrue(config.cookiebot_enabled)
