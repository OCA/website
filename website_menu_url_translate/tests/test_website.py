# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl)


from odoo.tests.common import HttpCase, TransactionCase

CONTROLLER_PATH = "odoo.addons.website_sale_affiliate.controllers.main"


class WebsiteSaleCase(HttpCase, TransactionCase):
    def setUp(self):
        super(WebsiteSaleCase, self).setUp()
        self.test1 = self.env.ref("website_menu_url_translate.lang_change_test_1")
        self.test2 = self.env.ref("website_menu_url_translate.lang_change_test_2")

    def test_change_lang(self):
        """Test change_lang controller with default language"""
        data = {
            "url": "/website/lang/{}".format("default"),
        }
        req = self.url_open("%(url)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
        # Test with english language
        data = {
            "url": "/website/lang/{}".format("en_US"),
            "r": "testen",
        }
        req = self.url_open("%(url)s?r=%(r)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
        # Test with german language
        data = {
            "url": "/website/lang/{}".format("de_DE"),
            "r": "Testing",
        }
        req = self.url_open("%(url)s?r=%(r)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
        # Test with german language
        data = {
            "url": "/website/lang/{}".format("es_ES"),
            "r": "",
        }
        req = self.url_open("%(url)s?r=%(r)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
        # Test with English language
        data = {
            "url": "/website/lang/{}".format("en_US"),
            "r": "",
        }
        req = self.url_open("%(url)s?r=%(r)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
        # Test with german language
        data = {
            "url": "/website/lang/{}".format("de_DE"),
            "r": "",
        }
        req = self.url_open("%(url)s?r=%(r)s" % data, allow_redirects=False)
        self.assertIn(req.status_code, [303, 200])
