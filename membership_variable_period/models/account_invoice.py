# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api, fields
from datetime import timedelta


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    membership_lines = fields.One2many(
        comodel_name='membership.membership_line',
        inverse_name='account_invoice_line')

    def _prepare_membership_line(self, invoice, product, price_unit, line_id):
        memb_line_model = self.env['membership.membership_line']
        memb_lines = memb_line_model.search(
            [('partner', '=', invoice.partner_id.id)],
            order="date_to desc")
        if memb_lines and memb_lines[0].date_to:
            date_from = (fields.Date.from_string(memb_lines[0].date_to) +
                         timedelta(days=1))
        else:
            date_from = fields.Date.from_string(
                invoice.date_invoice or fields.Date.today())
        date_to = (product.product_tmpl_id._get_next_date(date_from) -
                   timedelta(days=1))
        return {
            'partner': invoice.partner_id.id,
            'membership_id': product.id,
            'member_price': price_unit,
            'date': fields.Date.today(),
            'date_from': fields.Date.to_string(date_from),
            'date_to': fields.Date.to_string(date_to),
            'state': 'waiting',
            'account_invoice_line': line_id,
        }

    @api.multi
    def write(self, vals):
        """Create before the lines of membership with variable period."""
        memb_line_model = self.env['membership.membership_line']
        if vals.get('product_id') or vals.get('quantity'):
            for line in self:
                if vals.get('product_id'):
                    product = self.env['product.product'].browse(
                        vals['product_id'])
                else:
                    product = line.product_id
                if vals.get('invoice_id'):
                    invoice = self.env['account.invoice'].browse(
                        vals['invoice_id'])
                else:
                    invoice = line.invoice_id
                if (invoice.type == 'out_invoice' and
                        product.membership and
                        product.membership_type == 'variable'):
                    quantity = vals.get('quantity', line.quantity)
                    memb_lines = memb_line_model.search(
                        [('account_invoice_line', '=', line.id)],
                        order="date desc, id desc")
                    if len(memb_lines) < quantity:
                        # Add missing membership lines
                        price_unit = vals.get('price_unit', line.price_unit)
                        missing_number = quantity - len(memb_lines)
                        for i in range(int(missing_number)):
                            membership_vals = self._prepare_membership_line(
                                invoice, product, price_unit, line.id)
                            memb_line_model.create(membership_vals)
                    elif len(memb_lines) > quantity:
                        # Remove extra membership lines
                        extra_number = len(memb_lines) - quantity
                        memb_lines[:extra_number].unlink()
        return super(AccountInvoiceLine, self).write(vals)

    @api.model
    def create(self, vals):
        memb_line_model = self.env['membership.membership_line']
        price_unit = vals.get('price_unit', 0.0)
        line = super(AccountInvoiceLine, self).create(vals)
        if (line.invoice_id.type == 'out_invoice' and
                line.product_id.membership and
                line.product_id.membership_type == 'variable'):
            for i in range(int(line.quantity)):
                membership_vals = self._prepare_membership_line(
                    line.invoice_id, line.product_id, price_unit, line.id)
                if line.membership_lines:
                    # There's already the super line
                    line.membership_lines[0].write(membership_vals)
                else:
                    memb_line_model.create(membership_vals)
        return line
