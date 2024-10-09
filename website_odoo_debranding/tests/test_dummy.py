from odoo.tests.common import TransactionCase


class TestDummy(TransactionCase):
    def test_dummy(self):
        """Dummy test to avoid warnings"""
        self.assertTrue(True)
