# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
#                 Antonio Espinosa <antonioea@antiun.com>
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

from openerp import http
from openerp.http import request
from openerp.addons.website_sale.controllers.main import website_sale


class WebsiteSale(website_sale):

    @http.route(['/shop/get_unit_price'], type='json', auth="public",
                methods=['POST'], website=True)
    def get_unit_price(self, product_ids, add_qty,
                       use_order_pricelist=False, **kw):
        result = super(WebsiteSale, self).get_unit_price(
            product_ids, add_qty,
            use_order_pricelist=use_order_pricelist, **kw)
        if result and type(result) is dict:
            prices = {}
            m_product = request.env['product.product'].sudo()
            for product_id, price in result.iteritems():
                product = m_product.browse(product_id)
                if product:
                    taxes = product.sudo().taxes_id.compute_all(
                        price, 1, product=product)
                    prices[product_id] = taxes['total_included']
            result = prices
        return result
