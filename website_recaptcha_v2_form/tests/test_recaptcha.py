from unittest import mock

from odoo.exceptions import AccessDenied
from odoo.tests import common

imp_requests = "odoo.addons.website_recaptcha_v2.models.website.requests"


class TestModule(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.website.write(
            {
                "recaptcha_v2_enabled": True,
                "recaptcha_v2_site_key": "test-site",
                "recaptcha_v2_secret_key": "test-secret",
            }
        )
        cls.other_recaptcha_v2_site_key = "other-test-site"
        cls.view_test_recaptcha = cls.env["ir.ui.view"].create(
            {
                "name": "Test Recaptcha",
                "type": "qweb",
                "arch": """
                <t name="Test Recaptcha">
                <div class="g-recaptcha" t-att-data-sitekey="%s"
                data-callback="callback_success_recaptcha"
                data-expired-callback="callback_expired_recaptcha"/>
            <div>Test Recaptcha</div>
                </t>
            """
                % cls.website.recaptcha_v2_site_key,
            }
        )
        cls.ResConfigSettings = cls.env["res.config.settings"]

    @mock.patch(imp_requests)
    def test_captcha_valid(self, requests_mock):
        requests_mock.post().json.return_value = {"success": True}
        result = self.website.valid_recaptcha(
            {"g-recaptcha-response": "dummy_response"}
        )
        self.assertTrue(result)

    @mock.patch(imp_requests)
    def test_captcha_not_valid(self, requests_mock):
        requests_mock.post().json.return_value = {"success": False}
        with self.assertRaises(AccessDenied):
            self.website.valid_recaptcha({"g-recaptcha-response": ""})

    def test_valid_recaptcha_v2_site_key(self):
        recaptcha_v2_site_key = self.website.recaptcha_v2_site_key
        self.assertEqual(recaptcha_v2_site_key, "test-site")
        recaptcha_v2_site_key = ""
        self.assertNotEqual(
            recaptcha_v2_site_key,
            "test-site",
            msg="The website key for recaptcha is empty.",
        )
        recaptcha_v2_site_key = self.website.get_recaptcha_v2_site_key()
        self.assertNotEqual(recaptcha_v2_site_key, "")

    def test_valid_recaptcha_v2_recaptcha_v2_secret_key(self):
        recaptcha_v2_secret_key = self.website.recaptcha_v2_secret_key
        self.assertEqual(recaptcha_v2_secret_key, "test-secret")
        recaptcha_v2_secret_key = ""
        self.assertNotEqual(
            recaptcha_v2_secret_key,
            "test-site",
            msg="The website key for recaptcha is empty.",
        )

    def test_update_recaptcha(self):
        arch_db = self.view_test_recaptcha.arch_db
        site_key_old = arch_db.split('data-sitekey="')
        self.assertEqual(len(site_key_old), 2)
        site_key = site_key_old[1].split('"')
        self.assertGreaterEqual(len(site_key), 1)

    def test_update_recaptcha_v2_site_key(self):
        html_original = (
            '<div class="g-recaptcha" data-sitekey="OLD_KEY_ABC" '
            'data-callback="callback_success_recaptcha" '
            'data-expired-callback="callback_expired_recaptcha"/>'
        )
        view = self.env["ir.ui.view"].create(
            {
                "name": "Fake Recaptcha View",
                "type": "qweb",
                "arch": html_original,
                "arch_db": html_original,
                "website_id": self.env["website"].create({"name": "Test Site"}).id,
            }
        )
        self.website.update_recaptcha_v2_site_key()
        self.assertIn("test-site", view.arch_db)
        self.assertNotIn("OLD_KEY_ABC", view.arch_db)
