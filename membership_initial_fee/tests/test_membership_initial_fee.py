# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestAccountPaymentTermMultiDay(common.TransactionCase):

    def setUp(self):
        super(TestAccountPaymentTermMultiDay, self).setUp()
        self.product_fixed = self.env['product.product'].create(
            {
                'name': 'Membership product with fixed initial fee',
                'membership': True,
                'initial_fee': 'fixed',
                'fixed_fee': 50.0,
                'list_price': 150.0,
            })
        self.product_percentage = self.env['product.product'].create(
            {
                'name': 'Membership product with percentage initial fee',
                'membership': True,
                'initial_fee': 'percentage',
                'percentage_fee': 10.0,
                'list_price': 150.0,
            })
        self.partner = self.env['res.partner'].create({'name': 'Test'})

    def check_membership_invoice(self, invoice, expected_amount):
        self.assertEqual(
            len(invoice.invoice_line), 2,
            "The created invoice should have 2 lines")
        initial_fee_line = invoice.invoice_line.filtered(
            lambda x: not x.product_id)
        self.assertEqual(
            initial_fee_line.price_unit, expected_amount,
            "The initial fee amount is not correct")

    def test_create_invoice_initial_fee_fixed(self):
        invoice_id = self.partner.create_membership_invoice(
            product_id=self.product_fixed.id, datas={})[0]
        invoice = self.env['account.invoice'].browse(invoice_id)
        self.check_membership_invoice(invoice, 50.0)

    def test_create_invoice_initial_fee_percentage(self):
        invoice_id = self.partner.create_membership_invoice(
            product_id=self.product_percentage.id,
            datas={'amount': 150.0})[0]
        invoice = self.env['account.invoice'].browse(invoice_id)
        self.check_membership_invoice(invoice, 15.0)
