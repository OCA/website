# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.models import Model
from openerp import fields
from openerp import SUPERUSER_ID
from openerp.addons import decimal_precision

import logging
_logger = logging.getLogger(__name__)


class sale_order(Model):

    """Overwrites and add Definitions to module: sale."""

    _inherit = 'sale.order'

    def _amount_all_wrapper(self, cr, uid, ids, field_name, arg, context=None):
        """
        Overwrites module: sale.

        Call original _amount_all_wrapper() function via super() function for
        function field.
        """
        return super(sale_order, self)._amount_all_wrapper(cr, uid, ids, field_name, arg, context)

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        """
        Overwrites module: sale.

        Call original _amount_all() function and extend it with new subtotal
        calculation.
        """
        res = super(sale_order, self)._amount_all(cr, uid, ids, field_name, arg, context=context)

        currency_pool = self.pool.get('res.currency')
        for order in self.browse(cr, uid, ids, context=context):
            line_amount = sum([line.price_subtotal for line in order.order_line if
                               line.is_delivery is False])
            currency = order.pricelist_id.currency_id
            res[order.id]['amount_subtotal'] = currency_pool.round(cr, uid, currency, line_amount)

        return res

    def _get_order(self, cr, uid, ids, context=None):
        """
        Overwrites module: sale.

        Call original _get_order() function for function field.

        Important: We can't use super() function here because of getting an
        TypeError when adding or deleting products in cart: (TypeError:
        super(type, obj): obj must be an instance or subtype of type).
        """
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()

    amount_subtotal = fields.Float(
        compute=_amount_all_wrapper,
        digits_compute=decimal_precision.get_precision('Account'),
        string='Subtotal Amount',
        store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount',
                                                 'product_uom_qty'], 10),},
        multi='sums',
        help="The amount without anything.",
        track_visibility='always'
        )
    
    def tax_overview(self, cr, uid, order, context=None):
        """
        Calculate additional tax information for displaying them in
        onestepcheckout page.
        """
        taxes = {}
        for line in order.order_line:
            for tax in line.tax_id:
                if str(tax.id) in taxes:
                    taxes[str(tax.id)]['value'] += self._amount_line_tax(cr, uid, line,
                                                                         context=context)
                else:
                    taxes[str(tax.id)] = {'label': tax.name, 'value': self._amount_line_tax(
                        cr, uid, line, context=context)}

        # round and formatting valid taxes
        res = []
        rc_obj = self.pool.get('res.currency')
        currency = order.pricelist_id.currency_id
        for key in taxes:
            if taxes[key]['value'] > 0:
                taxes[key]['value'] = '%.2f' % rc_obj.round(cr, uid, currency, taxes[key]['value'])
                res.append(taxes[key])

        return res


class res_partner(Model):
    _inherit = 'res.partner'

    street_name = fields.Char(string='Street name')
    street_number = fields.Char(tring='Street number')
