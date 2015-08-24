# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api, fields
from datetime import timedelta


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _get_membership_interval(self, product, date):
        """Get the interval to evaluate as the theoretical membership period.
        :param product: Product that defines the membership
        :param date: date object for the requested date (if needed for
        inherited computations)
        :return: A tuple with 2 date objects with the beginning and the
        end of the period
        """
        date_from = fields.Date.from_string(product.membership_date_from)
        date_to = fields.Date.from_string(product.membership_date_to)
        return date_from, date_to

    def _prepare_invoice_line_prorrate_vals(self, invoice_line):
        product = invoice_line.product_id
        date_invoice = fields.Date.from_string(
            invoice_line.invoice_id.date_invoice or fields.Date.today())
        date_from, date_to = self._get_membership_interval(
            product, date_invoice)
        if date_invoice < date_from:
            date_invoice = date_from
        if date_invoice > date_to:
            date_invoice = date_to
        theoretical_duration = date_to - date_from + timedelta(1)
        real_duration = date_to - date_invoice
        if theoretical_duration != real_duration:
            return {
                'quantity': (float(real_duration.days) /
                             theoretical_duration.days)
            }
        return {}

    @api.model
    def create(self, vals):
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        if (self.env.context.get('no_initial_fee_check') or not
                vals.get('product_id')):
            return invoice_line
        product = self.env['product.product'].browse(vals['product_id'])
        if not product.membership or not product.membership_prorrate:
            return invoice_line
        # Change quantity accordingly the prorrate
        invoice_line_vals = self._prepare_invoice_line_prorrate_vals(
            invoice_line)
        if invoice_line_vals:
            invoice_line.write(invoice_line_vals)
        return invoice_line
