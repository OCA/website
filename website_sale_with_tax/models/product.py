# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_with_tax = fields.Float(
        string="Price with tax", compute="_get_product_total_price_with_tax")

    @api.one
    def _get_product_total_price_with_tax(self):
        # TODO implement with compute_all
        # taxes = self.env['account.tax'].compute_all(
        #     self.price, 1, product=self)
        sum_tax = 0
        for tax in self.taxes_id:
            sum_tax += self.price * tax.amount
        self.price_with_tax = ('%.2f' % (self.price + sum_tax))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    price_with_tax = fields.Float(
        string="Price with tax", compute="_get_product_total_price_with_tax")

    @api.one
    def _get_product_total_price_with_tax(self):
        sum_tax = 0
        for tax in self.taxes_id:
            sum_tax += self.lst_price * tax.amount
        self.price_with_tax = ('%.2f' % (self.lst_price + sum_tax))
