# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
#    Copyright (C) 2014 initOS GmbH & Co. KG (<http://www.initos.com>).
#    Author Markus Schneider <markus.schneider at initos.com>
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


class website_doc_api(http.Controller):

    @http.route(['/doc/jsonrpc'], type='http', auth="public", website=True)
    def doc_jsonrpc(self, **searches):
        model_obj = request.registry['ir.model']

        obj_ids = model_obj.search(
            request.cr, request.uid, [(1, '=', 1)], context=request.context)
        model_ids = model_obj.browse(request.cr, request.uid, obj_ids,
                                     context=request.context)
        values = {
            'model_ids': model_ids
        }
        return http.request.render("website_doc_jsonrpc.index", values)

    @http.route(['/doc/jsonrpc/<model("ir.model"):model>'], type='http', auth="public", website=True)
    def doc_jsonrpc_model(self, model, **searches):
        model_obj = request.registry['ir.model']

        obj_ids = model_obj.search(
            request.cr, request.uid, [(1, '=', 1)], context=request.context)
        model_ids = model_obj.browse(request.cr, request.uid, obj_ids,
                                     context=request.context)
        values = {
            'model_ids': model,
            'all_models': model_ids
        }
        return http.request.render("website_doc_jsonrpc.single", values)
