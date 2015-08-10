# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def write(self, vals):
        # This is a workaround for avoiding the overwriting of the invoice line
        # Part 2: if a write operation with the context variable is detected,
        # don't make the write - See https://github.com/odoo/odoo/pull/7971
        if (self.env.context.get('create_membership_invoice') and
                len(vals) == 1 and vals.get('invoice_line')):
            return True
        return super(AccountInvoice, self).write(vals)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    def _prepare_initial_fee_vals(self, invoice_line):
        product = invoice_line.product_id
        line_vals = {
            'quantity': 1.0,
            'invoice_id': invoice_line.invoice_id.id,
        }
        line_dict = self.product_id_change(
            product.id, False, line_vals['quantity'], '',
            'out_invoice', invoice_line.invoice_id.partner_id.id,
            invoice_line.invoice_id.fiscal_position.id)
        line_vals.update(line_dict['value'])
        if product.initial_fee == 'fixed':
            line_vals['price_unit'] = product.fixed_fee
        elif product.initial_fee == 'percentage':
            line_vals['price_unit'] = (
                product.percentage_fee * invoice_line.price_unit / 100)
        line_vals['name'] = _('Membership initial fee')
        if line_vals.get('invoice_line_tax_id', False):
            line_vals['invoice_line_tax_id'] = [
                (6, 0, line_vals['invoice_line_tax_id'])]
        return line_vals

    @api.model
    def create(self, vals):
        invoice_line = super(AccountInvoiceLine, self).create(vals)
        if (self.env.context.get('no_initial_fee_check') or not
                vals.get('product_id')):
            return invoice_line
        product = self.env['product.product'].browse(vals['product_id'])
        if not product.membership or product.initial_fee == 'none':
            return invoice_line
        # See if this is the first invoice
        invoices = self.env['account.invoice'].search(
            [('partner_id', '=', invoice_line.invoice_id.partner_id.id),
             ('state', 'in', ('draft', 'open', 'paid')),
             ('invoice_line.product_id', '=', product.id)])
        if len(invoices) == 1:
            # Charge initial fee
            self.create(self._prepare_initial_fee_vals(invoice_line))
        return invoice_line
