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
from openerp import api, fields, models
from openerp.addons import decimal_precision


class SaleOrder(models.Model):

    """Overwrites and add Definitions to module: sale."""

    _inherit = 'sale.order'

    @api.model
    def tax_overview(self, order):
        """
        Calculate additional tax information for displaying them in
        onestepcheckout page.
        """
        taxes = {}
        for line in order.order_line:
            for tax in line.tax_id:
                if str(tax.id) in taxes:
                    taxes[str(tax.id)]['value'] += self._amount_line_tax(line)
                else:
                    taxes[str(tax.id)] = {'label': tax.name,
                                          'value': self._amount_line_tax(line)}

        # round and formatting valid taxes
        res = []
        currency = order.pricelist_id.currency_id
        for key in taxes:
            if taxes[key]['value'] > 0:
                taxes[key]['value'] = '%.2f' % currency.round(taxes[key][
                    'value'])
                res.append(taxes[key])

        return res


class ResPartner(models.Model):

    """Add Fields to res.partner."""

    _inherit = 'res.partner'

    street_name = fields.Char(string='Street name')
    street_number = fields.Char(tring='Street number')
