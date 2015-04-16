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

from openerp.addons.website_sale_options.controllers.main import (
    website_sale_options)
from openerp.addons.web import http
from openerp.addons.web.http import request


class website_unsaleable_options(website_sale_options):

    @http.route()
    def modal(self, product_id, **kw):
        cr, uid, context, pool = (
            request.cr, request.uid, request.context, request.registry)
        template = pool['product.template']
        cr.execute(
            "select src_id from product_optional_rel where dest_id"
            " = %s"
            % product_id)
        res = cr.fetchall()
        if res:
            products = template.browse(
                cr, uid, [item[0] for item in res], context)
            prod_list = [p.name for p in products]
            message = ("You can't direcly add to cart an optional "
                       "product. You should first add one of the "
                       "following products:\n"
                       "%s" % '\n'.join(prod_list))
            return request.website._render(
                "website_unsaleable_options.modal_warning", {
                    'message': message,
                    })
        else:
            return super(website_unsaleable_options, self).modal(
                product_id, **kw)
