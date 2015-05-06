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
from openerp.tools.translate import _


class website_sale_unsaleable_options(website_sale_options):

    @http.route()
    def modal(self, product_id, **kw):
        cr, uid, context, pool = (
            request.cr, request.uid, request.context, request.registry)
        website_context = kw.get('kwargs', {}).get('context', {})
        context = dict(context or {}, **website_context)
        request.website = request.website.with_context(context)
        template = pool['product.template']
        prod_ids = template.search(
            cr, uid, [('optional_product_ids', 'in', [product_id])],
            context=context)
        if prod_ids:
            products = template.browse(
                cr, uid, prod_ids, context)
            prod_list = [p.name for p in products]
            message = _("You can't direcly add to cart an optional "
                        "product. You should first add one of the "
                        "following products: "
                        "%s") % '; '.join(prod_list)
            return request.website._render(
                "website_sale_unsaleable_options.modal_warning", {
                    'message': message,
                    })
        else:
            return super(website_sale_unsaleable_options, self).modal(
                product_id, **kw)
