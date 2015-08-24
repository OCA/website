# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestMembershipProrrateVariablePeriod(common.TransactionCase):

    def setUp(self):
        super(TestMembershipProrrateVariablePeriod, self).setUp()
        self.product = self.env['product.product'].create(
            {
                'name': 'Membership product with prorrate',
                'membership': True,
                'membership_prorrate': True,
                'membership_date_from': '2015-01-01',
                'membership_date_to': '2015-12-31',
                'membership_type': 'variable',
                'membership_interval_qty': 1,
                'membership_interval_unit': 'weeks',
            })
        self.partner = self.env['res.partner'].create({'name': 'Test'})

    def test_create_invoice_membership_product_wo_prorrate(self):
        self.membership_type = 'fixed'
        self.product.membership_prorrate = False
        invoice = self.env['account.invoice'].create(
            {'partner_id': self.partner.id,
             'date_invoice': '2015-07-01',
             'account_id': self.partner.property_account_receivable.id,
             'invoice_line': [(0, 0, {'product_id': self.product.id,
                                      'name': 'Membership w/o prorrate'})]}
        )
        self.assertEqual(invoice.invoice_line[0].quantity, 1.0)

    def test_create_invoice_membership_product_prorrate_week(self):
        invoice = self.env['account.invoice'].create(
            {'partner_id': self.partner.id,
             'date_invoice': '2015-01-01',  # It's thursday
             'account_id': self.partner.property_account_receivable.id,
             'invoice_line': [(0, 0, {'product_id': self.product.id,
                                      'name': 'Membership with prorrate'})]}
        )
        # Result is rounded to 2 decimals for avoiding the fail in tests
        # if "Product Unit of Measure" precision changes in the future
        self.assertEqual(round(invoice.invoice_line[0].quantity, 2), 0.43)

    def test_create_invoice_membership_product_prorrate_month(self):
        self.product.membership_interval_unit = 'months'
        invoice = self.env['account.invoice'].create(
            {'partner_id': self.partner.id,
             'date_invoice': '2015-04-15',
             'account_id': self.partner.property_account_receivable.id,
             'invoice_line': [(0, 0, {'product_id': self.product.id,
                                      'name': 'Membership with prorrate'})]}
        )
        # Result is rounded to 2 decimals for avoiding the fail in tests
        # if "Product Unit of Measure" precision changes in the future
        self.assertEqual(round(invoice.invoice_line[0].quantity, 2), 0.5)

    def test_create_invoice_membership_product_prorrate_year(self):
        self.product.membership_interval_unit = 'years'
        invoice = self.env['account.invoice'].create(
            {'partner_id': self.partner.id,
             'date_invoice': '2016-07-01',  # It's leap year
             'account_id': self.partner.property_account_receivable.id,
             'invoice_line': [(0, 0, {'product_id': self.product.id,
                                      'name': 'Membership with prorrate'})]}
        )
        # Result is rounded to 2 decimals for avoiding the fail in tests
        # if "Product Unit of Measure" precision changes in the future
        self.assertEqual(round(invoice.invoice_line[0].quantity, 2), 0.5)
