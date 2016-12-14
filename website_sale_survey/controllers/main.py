# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request


class website_sale_survey(http.Controller):

    @http.route(['/shop/survey'], type='http', auth="public", website=True)
    def shop_survey(self, **post):
        cr, uid, context = request.cr, request.uid, request.context
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            sale_obj = request.registry['sale.order']
            order = sale_obj.browse(
                cr, SUPERUSER_ID, sale_order_id, context=context)
            survey = order.survey_id
            if survey:
                vals = {'survey_id': survey.id,
                        'sale_order_id': order.id}
                if request.website.user_id.id != uid:
                    vals['partner_id'] = request.registry['res.users'].browse(
                        cr, uid, uid, context=context).partner_id.id
                user_input_obj = request.registry['survey.user_input']
                user_input_id = user_input_obj.create(
                    cr, uid, vals, context=context)
                user_input = user_input_obj.browse(
                    cr, uid, [user_input_id], context=context)[0]
                return request.redirect('/survey/fill/%s/%s' %
                                        (survey.id, user_input.token))
        return request.redirect('/shop')
