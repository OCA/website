# Copyright 2025 Simone Rubino - PyTech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import json

from odoo.tests import HttpCase
from odoo.tools import mute_logger


class TestIrHttp(HttpCase):
    def setUp(self):
        super().setUp()
        self.website = self.env["website"].sudo().get_current_website()
        self.auth_url = self.env["website.auth.url"].create(
            {"website_id": self.website.id, "path": "/contactus"}
        )
        self.user = self.env["res.users"].create(
            {"name": "Test User", "login": "test_user", "password": "12345"}
        )
        self.path = "/contactus"
        self.expected_path = "/web/login?redirect=%s" % self.path

    def test_dispatch_unauthorized(self):
        # Test that an unauthorized user cannot access "/auth_path
        self.authenticate(None, None)
        response = self.url_open(self.path, allow_redirects=False)
        self.assertEqual(
            response.status_code,
            302,
            "Expected the response status code to be 302 indicating a redirect",
        )

        self.assertIn(self.expected_path, response.headers["Location"])

    def test_dispatch_authorized(self):
        # Test that an authorized user can access "/auth_path
        self.authenticate(user="test_user", password="12345")
        response = self.url_open(self.path)
        self.assertEqual(
            response.status_code,
            200,
            "Expected the response status code to be 200 which means no redirection",
        )

    def test_dispatch_failed_transaction(self):
        """If a transaction is failed, the exception is handled as usual."""
        cron = self.env["ir.cron"].create(
            {
                "name": "Test failed transaction",
                "code": "env.cr.execute('SELECT not_a_field FROM res_users')",
                "model_id": self.env.ref("base.model_res_partner").id,
            }
        )
        self.authenticate(user="admin", password="admin")
        with mute_logger("odoo.sql_db", "odoo.http"):
            response = self.url_open(
                "/web/dataset/call_button",
                headers={
                    "Content-Type": "application/json",
                },
                data=json.dumps(
                    {
                        "params": {
                            "model": cron._name,
                            "method": "method_direct_trigger",
                            "args": [cron.ids],
                            "kwargs": {},
                        },
                    }
                ),
            )
        self.assertEqual(response.status_code, 200)
