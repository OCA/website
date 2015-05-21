# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def get_products_company(self):
        """
        Check products companies. If all products have the same company
        (or empty), return it
        If get_products_company doesn't find a unique company,
        the default one id used
        (returned by '_get_default_company' of 'sale.order')
        """
        companies = {}
        company = False
        for order in self:
            for line in order.order_line:
                if line.product_id and line.product_id.company_id:
                    companies[line.product_id.company_id] = True
        if len(companies) == 1:
            company = companies.keys()[0]
        return company
