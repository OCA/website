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

from openerp.osv import orm


class website(orm.Model):
    _inherit = 'website'

    def sale_get_order(
        self, cr, uid, ids, force_create=False, code=None,
        update_pricelist=None, context=None
    ):
        order = super(website, self).sale_get_order(
            cr, uid, ids, force_create=force_create, code=code,
            update_pricelist=update_pricelist, context=context)
        if order:
            company = order.get_products_company()
            if company:
                order.write({'company_id': company.id})
        return order
