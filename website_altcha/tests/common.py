# Copyright 2026 Dixmit
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import HttpCase, tagged


@tagged("-at_install", "post_install")
class Common(HttpCase):
    @classmethod
    def setUpClass(cls):
        result = super().setUpClass()
        cls.website = cls.env["website"].get_current_website()
        cls.website.altcha_key = "test_key"
        cls.website.altcha_private_key = "test_secret_key"
        cls.website.altcha_cost = 2
        # Forcing a small power of 2 cost for allowing scrypt to work
        # and make everything faster
        return result
