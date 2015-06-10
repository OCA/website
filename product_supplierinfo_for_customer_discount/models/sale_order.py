# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (c) 2014 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
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


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if not product:
            return res
        supplierinfo_obj = self.env['product.supplierinfo']
        product_obj = self.env['product.product']
        product_uom_obj = self.env['product.uom']
        pl_pinfo_obj = self.env['pricelist.partnerinfo']
        # Look for a possible discount
        product = product_obj.browse(product)
        from_uom = self.env.context.get('uom') or product.uom_id.id
        qty_in_product_uom = qty
        sinfos = supplierinfo_obj.search(
            [('product_tmpl_id', '=', product.product_tmpl_id.id),
             ('name', 'child_of', partner_id),
             ('type', '=', 'customer')])
        if not sinfos:
            return res
        seller_uom = sinfos.product_uom.id or False
        if seller_uom and from_uom and from_uom != seller_uom:
            qty_in_product_uom = product_uom_obj._compute_qty(
                from_uom, qty, to_uom_id=seller_uom)
        pl_pinfos = pl_pinfo_obj.search(
            [('suppinfo_id', 'in', sinfos.ids)], order="min_quantity")
        if 'value' not in res:
            res['value'] = {}
        for pl_pinfo in pl_pinfos:
            if pl_pinfo.min_quantity <= qty_in_product_uom:
                res['value']['discount'] = pl_pinfo.discount
            else:
                break
        return res
