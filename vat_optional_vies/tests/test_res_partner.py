# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning
from . import base


# One test case per method
class TestResPartner(base.BaseCase):
    # Use case : Prepare some data for current test case
    # def setUp(self):
    #     super(TestResPartner, self).setUp()
    #     # More initializations here ...

    # Use case : Clean data after current test case
    # def tearDown(self):
    #     # Clean data here ...
    #     super(TestResPartner, self).tearDown()

    def test_some_action(self):
        record = self.env['res.partner'].create({'name': 'Firstname Lastname'})
        self.assertTrue(record)

        # Use case: Test some action
        # record.some_action()
        # self.assertEqual(
        #     record.field,
        #     expected_field_value)

        # Use case: Test an exception
        # with self.assertRaises(Warning):
        #     self.env['res.partner'].create({'name': False})
