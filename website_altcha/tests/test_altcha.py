# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest import mock

from altcha.v2 import Challenge, Payload, solve_challenge
from freezegun import freeze_time
from requests.exceptions import HTTPError

from odoo.exceptions import UserError
from odoo.tests import Form
from odoo.tools import mute_logger

from odoo.addons.website.tools import MockRequest

from .common import Common


class TestAltchaCreation(Common):
    @classmethod
    def setUpClass(cls):
        result = super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.website.altcha_key = "test_key"
        cls.website.altcha_private_key = "test_secret_key"
        cls.website.altcha_cost = 128
        # Forcing a small power of 2 cost for allowing scrypt to work
        # and make everything faster
        return result

    def test_generate_altcha_challenge(self):
        response = self.url_open("/altcha")
        self.assertEqual(response.status_code, 200, "Expected status code 200")
        challenge = Challenge.from_dict(response.json())
        with MockRequest(self.env, website=self.website):
            self.assertTrue(
                self.env["altcha.key"]
                .sudo()
                .search(
                    [
                        (
                            "key",
                            "=",
                            self.env["ir.http"]._get_altcha_key(challenge.signature),
                        )
                    ]
                )
            )

    def generate_and_solve_challenge(self, website=None):
        with mock.patch.object(
            type(self.env["website"]),
            "get_current_website",
            return_value=website or self.website,
        ):
            response = self.url_open("/altcha")
            response.raise_for_status()
        challenge = Challenge.from_dict(response.json())
        return Payload(challenge, solve_challenge(challenge))

    def solve_altcha_challenge_ok(self, website=None):
        payload = self.generate_and_solve_challenge(website)
        with MockRequest(self.env, website=website or self.website) as request:
            request.params["altcha"] = payload.to_base64()
            self.env["ir.http"]._verify_request_recaptcha_token("TEST")
            self.assertTrue(
                self.env["altcha.key"]
                .sudo()
                .search(
                    [
                        (
                            "key",
                            "=",
                            self.env["ir.http"]._get_altcha_key(
                                payload.challenge.signature
                            ),
                        )
                    ]
                )
                .used
            )

    def test_generate_altcha_all_algorithms(self):
        for algorithm, _description in self.env["website"]._get_available_algorithms():
            with self.subTest(algorithm=algorithm):
                self.website.write({"altcha_algorithm": algorithm})
                self.solve_altcha_challenge_ok()

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_01(self):
        """Fails because Altcha is not passed"""
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = False
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_02(self):
        """Signature fails for wrong signature"""
        payload = self.generate_and_solve_challenge()
        payload.challenge.signature = "invalid_signature"
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = payload.to_base64()
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_03(self):
        """Signature fails with wrong payload"""
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = "Not a valid ALTCHA Base64"
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_04(self):
        """Signature fails with wrong solution"""
        payload = self.generate_and_solve_challenge()
        payload.solution.derived_key += "01"
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = payload.to_base64()
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_05(self):
        """Signature fails when expired"""
        with freeze_time("2026-01-01 00:00:00"):
            payload = self.generate_and_solve_challenge()
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = payload.to_base64()
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    @mute_logger("odoo.addons.website_altcha.models.ir_http")
    def test_solve_altcha_challenge_failure_06(self):
        """Signature fails when reused"""
        payload = self.generate_and_solve_challenge()
        with MockRequest(self.env, website=self.website) as request:
            request.params["altcha"] = payload.to_base64()
            self.env["ir.http"]._verify_request_recaptcha_token("TEST")
            with self.assertRaises(UserError):
                self.env["ir.http"]._verify_request_recaptcha_token("TEST")

    def test_autovacuum(self):
        with freeze_time("2026-01-01 00:00:00"):
            payload = self.generate_and_solve_challenge()
        with MockRequest(self.env, website=self.website):
            key = (
                self.env["altcha.key"]
                .sudo()
                .search(
                    [
                        (
                            "key",
                            "=",
                            self.env["ir.http"]._get_altcha_key(
                                payload.challenge.signature
                            ),
                        )
                    ]
                )
            )
        self.assertTrue(key)
        self.env["altcha.key"].sudo()._autovacuum_expired_keys()
        self.assertFalse(key.exists())

    def test_no_altcha_key_different_website(self):
        """Test that a challenge from another website is not valid"""
        # Create a second website without altcha keys
        website = self.env["website"].create(
            {
                "name": "Test Website 2",
                "domain": "test2",
                "altcha_cost": 128,
            }
        )
        self.solve_altcha_challenge_ok()
        with self.assertRaises(HTTPError), mute_logger("odoo.http"):
            # The challenge should fail for website2 which has no altcha key configured
            self.solve_altcha_challenge_ok(website=website)

    def test_altcha_configure_new_website(self):
        website = self.env["website"].create(
            {
                "name": "Test Website 2",
                "domain": "test2",
                "altcha_cost": 128,
            }
        )
        self.solve_altcha_challenge_ok()
        self.assertFalse(website.altcha_key, "Expected no altcha key for website 2")
        self.assertFalse(
            website.altcha_private_key, "Expected no altcha key for website 2"
        )
        with Form(self.env["res.config.settings"]) as f:
            f.website_id = website
            self.assertFalse(f.altcha_enabled)
            f.altcha_enabled = True
        self.assertTrue(
            website.altcha_key, "Expected altcha key to be generated for website 2"
        )
        self.assertTrue(
            website.altcha_private_key,
            "Expected altcha private key to be generated for website 2",
        )
        website.flush_recordset()
        self.solve_altcha_challenge_ok(website=website)
