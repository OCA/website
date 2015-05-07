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
# -*- coding: utf-8 -*-
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.report import report_sxw

import logging
logger = logging.getLogger(__name__)


class website_sale(website_sale):

    mandatory_billing_fields = ["name", "phone", "email", "street", "city", "country_id"]
    optional_billing_fields = ["street2", "state_id", "vat", "vat_subjected", "zip"]

    @http.route(['/shop/checkout'], type='http', auth='public', website=True, multilang=True)
    def checkout(self, **post):
        """"""
        # if onestepcheckout is deactivated use the normal checkout
        if not request.website.use_osc:
            return super(website_sale, self).checkout()

        # -------------------------------------------------------------------- #
        #                                                                      #
        #                       Checkout Part                                  #
        #                                                                      #
        # -------------------------------------------------------------------- #
        cr, uid, context, registry, website = request.cr, request.uid, request.context, \
                                              request.registry, request.website

        # must have a draft sale order with lines at this point, otherwise reset
        order = request.website.sale_get_order()
        if not order or order.state != 'draft' or not order.order_line:
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')
        # if transaction pending / done: redirect to confirmation
        tx = context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order.id)

        self.get_pricelist()

        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        orm_country = registry.get('res.country')
        state_orm = registry.get('res.country.state')
        states_ids = state_orm.search(cr, SUPERUSER_ID, [], context=context)
        states = state_orm.browse(cr, SUPERUSER_ID, states_ids, context)
        partner = orm_user.browse(cr, SUPERUSER_ID, request.uid, context).partner_id

        # get countries dependent on website settings
        country_ids = []
        if website.use_all_checkout_countries:
            country_ids = orm_country.search(cr, SUPERUSER_ID, [], context=context)
        else:
            country_ids = orm_country.search(
                cr, SUPERUSER_ID, [('id', 'in', [c.id for c in website.checkout_country_ids])],
                context=context)
        countries = orm_country.browse(cr, SUPERUSER_ID, country_ids, context)

        shipping_id = None
        shipping_ids = []
        checkout = {}

        if not post:
            if request.uid != request.website.user_id.id:
                checkout.update(self.checkout_parse('billing', partner))
                checkout.update({'street': partner.street_name,
                                 'street_number': partner.street_number})

                shipping_ids = orm_partner.search(
                    cr, SUPERUSER_ID,
                    [("parent_id", "=", partner.id),
                     ('type', "=", 'delivery')],
                    context=context)
            else:
                order = website.sale_get_order(force_create=1, context=context)
                if order.partner_id:
                    domain = [("active", "=", False), ("partner_id", "=", order.partner_id.id)]
                    user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID, domain,
                                                                    context=context)
                    if not user_ids or request.website.user_id.id not in user_ids:
                        checkout.update(self.checkout_parse("billing", order.partner_id))
        else:
            checkout = self.checkout_parse('billing', post)
            try:
                shipping_id = int(post["shipping_id"])
            except ValueError:
                pass
            if shipping_id == -1:
                checkout.update(self.checkout_parse('shipping', post))

        if shipping_id is None:
            if not order:
                order = request.website.sale_get_order(context=context)
            if order and order.partner_shipping_id:
                shipping_id = order.partner_shipping_id.id

        shipping_ids = list(set(shipping_ids) - set([partner.id]))

        if shipping_id == partner.id:
            shipping_id = 0
        elif shipping_id > 0 and shipping_id not in shipping_ids:
            shipping_ids.append(shipping_id)
        elif shipping_id is None and shipping_ids:
            shipping_id = shipping_ids[0]

        ctx = dict(context, show_address=1)
        shippings = []
        if shipping_ids:
            shippings = shipping_ids and orm_partner.browse(
                cr, SUPERUSER_ID, list(shipping_ids), ctx) or []
        if shipping_id > 0:
            shipping = orm_partner.browse(cr, SUPERUSER_ID, shipping_id, ctx)
            checkout.update(self.checkout_parse("shipping", shipping))

        checkout['shipping_id'] = shipping_id

        values = {
            'countries': countries,
            'states': states,
            'checkout': checkout,
            'shipping_id': partner.id != shipping_id and shipping_id or 0,
            'shippings': shippings,
            'error': {},
        }

        # -------------------------------------------------------------------- #
        #                                                                      #
        #                       Payment Part                                   #
        #                                                                      #
        # -------------------------------------------------------------------- #
        payment_obj = request.registry.get('payment.acquirer')

        # alread a transaction: forward to confirmation
        if tx and tx.state != 'draft':
            return request.redirect('/shop/confirmation/%s' % order.id)

        shipping_partner_id = False
        if order:
            if order.partner_shipping_id.id:
                shipping_partner_id = order.partner_shipping_id.id
            else:
                shipping_partner_id = order.partner_invoice_id.id

        values['order'] = request.registry['sale.order'].browse(cr, SUPERUSER_ID, order.id,
                                                                context=context)
        values.update(request.registry.get('sale.order')._get_website_data(cr, uid, order, context))

        # we don't want to use the public user for further processes
        if not partner and values.get('partner', False):
            del values['partner']

        # fetch all registered payment means
        # if tx:
        #     acquirer_ids = [tx.acquirer_id.id]
        # else:
        acquirer_ids = payment_obj.search(cr, SUPERUSER_ID, [('website_published', '=', True)],
                                          context=context)
        values['acquirers'] = list(payment_obj.browse(cr, uid, acquirer_ids, context=context))
        render_ctx = dict(context, submit_class='btn btn-primary', submit_txt='Order Now')
        for acquirer in values['acquirers']:
            acquirer.button = payment_obj.render(
                cr, SUPERUSER_ID, acquirer.id,
                order.name,
                order.amount_total,
                order.pricelist_id.currency_id.id,
                partner_id=shipping_partner_id,
                tx_values={
                    'return_url': '/shop/payment/validate',
                },
                context=render_ctx)

        # get additional tax information
        values['tax_overview'] = registry['sale.order'].tax_overview(cr, uid, order, context)
        return request.website.render('website_sale_osc.osc_onestepcheckout', values)

    @http.route(['/shop/checkout/confirm_address/'], type='json', auth='public', website=True,
                multilang=True)
    def confirm_address(self, **post):
        """
        """
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        order_line_obj = request.registry.get('sale.order')

        # must have a draft sale order with lines at this point, otherwise redirect to shop
        order = request.website.sale_get_order()
        if not order or order.state != 'draft' or not order.order_line:
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            logger.warn(' --- redirect shop')
            return request.redirect('/shop')
        # if transaction pending / done: redirect to confirmation
        tx = context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            logger.warn(' --- redirect confirmation')
            return request.redirect('/shop/payment/confirmation/%s' % order.id)

        orm_partner = registry.get('res.partner')
        orm_user = registry.get('res.users')
        orm_country = registry.get('res.country')
        country_ids = orm_country.search(cr, SUPERUSER_ID, [], context=context)
        countries = orm_country.browse(cr, SUPERUSER_ID, country_ids, context)
        orm_state = registry.get('res.country.state')
        states_ids = orm_state.search(cr, SUPERUSER_ID, [], context=context)
        states = orm_state.browse(cr, SUPERUSER_ID, states_ids, context)

        logger.info(' --- post')
        logger.info(post)
        info = {}
        values = {
            'countries': countries,
            'states': states,
            'checkout': info,
            'shipping': post.get('shipping_different')
        }
        checkout = values['checkout']
        checkout.update(post)

        logger.info(' --- checkout')
        logger.info(checkout)
        values['error'] = self.checkout_form_validate(values['checkout'])
        if values['error']:
            return {
                'success': False,
                'errors': values['error']
            }

        company_name = ''
        if 'company' in checkout:
            company_name = checkout['company']
        company_id = None

        if 'company' in post and post['company']:
            company_ids = orm_partner.search(cr, SUPERUSER_ID, [('name', 'ilike', company_name),
                                                                ('is_company', '=', True)],
                                             context=context)
            company_id = (company_ids and company_ids[0]) or orm_partner.create(
                cr, SUPERUSER_ID, {'name': company_name, 'is_company': True}, context)

        checkout['street_name'] = checkout.get('street')
        if checkout.get('street_number'):
            checkout['street'] = checkout.get('street') + ' ' + checkout.get('street_number')

        billing_info = dict((k, v) for k, v in checkout.items() if 'shipping_' not in k and k !=
                            'company')
        billing_info['parent_id'] = company_id
        partner_id = None

        if request.uid != request.website.user_id.id:
            partner_id = orm_user.browse(cr, SUPERUSER_ID, uid, context=context).partner_id.id
        elif order.partner_id:
            domain = [('active', '=', False), ('partner_id', '=', order.partner_id.id)]
            user_ids = request.registry['res.users'].search(cr, SUPERUSER_ID, domain,
                                                            context=context)
            if not user_ids or request.website.user_id.id not in user_ids:
                partner_id = order.partner_id.id

        if partner_id:
            orm_partner.write(cr, SUPERUSER_ID, [partner_id], billing_info, context=context)
        else:
            partner_id = orm_partner.create(cr, SUPERUSER_ID, billing_info, context=context)
        shipping_id = None
        logger.info(checkout.get('shipping_id'))
        if int(checkout.get('shipping_id')) == -1:
            shipping_info = {
                'phone': post['shipping_phone'],
                'zip': post['shipping_zip'],
                'street': post['shipping_street'] + ' ' + post.get('shipping_street_number'),
                'street_name': post['shipping_street'],
                'street_number': post['shipping_street_number'],
                'city': post['shipping_city'],
                'name': post['shipping_name'],
                'email': post['email'],
                'type': 'delivery',
                'parent_id': partner_id,
                'country_id': post['shipping_country_id'],
                'state_id': post['shipping_state_id'],
            }
            domain = [(key, '_id' in key and '=' or 'ilike', '_id' in key and value and int(
                value) or value)
                      for key, value in shipping_info.items() if key in
                      self.mandatory_billing_fields + ['type', 'parent_id']]
            shipping_ids = orm_partner.search(cr, SUPERUSER_ID, domain, context=context)
            logger.info(' --- shipping_ids')
            logger.info(shipping_ids)
            if shipping_ids:
                shipping_id = shipping_ids[0]
                orm_partner.write(cr, SUPERUSER_ID, [shipping_id], shipping_info, context)
            else:
                shipping_id = orm_partner.create(cr, SUPERUSER_ID, shipping_info, context)

        order_info = {
            'partner_id': partner_id,
            'message_follower_ids': [(4, partner_id), (3, request.website.partner_id.id)],
            'partner_invoice_id': partner_id
        }
        order_info.update(registry.get('sale.order').onchange_partner_id(cr, SUPERUSER_ID, [],
                                                                         partner_id,
                                                                         context=context)['value'])
        # we need to update partner_shipping_id after onchange_partner_id() call
        # otherwise the deselection of the option 'Ship to a different address'
        # would be overwritten by an existing shipping partner type
        order_info.update({'partner_shipping_id': shipping_id or partner_id})
        order_info.pop('user_id')

        order_line_obj.write(cr, SUPERUSER_ID, [order.id], order_info, context=context)
        request.session['sale_last_order_id'] = order.id
        logger.info(' --- success')
        return {'success': True}

    def do_change_delivery(self, cr, uid, order, carrier_id, context=None):
        """
        Apply delivery amount to current sale order.
        """

        if order and carrier_id:

            # order_id is needed to get delivery carrier price
            if not context.get('order_id'):
                context['order_id'] = order.id
                request.context['order_id'] = order.id

            # recompute delivery costs
            request.registry['sale.order']._check_carrier_quotation(cr, uid, order,
                                                                    force_carrier_id=carrier_id,
                                                                    context=context)

            # generate updated total prices
            updated_order = request.website.sale_get_order()
            product_pool = request.registry.get('product.product')
            rml_obj = report_sxw.rml_parse(cr, SUPERUSER_ID, product_pool._name, context=context)
            price_digits = rml_obj.get_digits(dp='Product Price')

            # get additional tax information
            tax_overview = request.registry['sale.order'].tax_overview(cr, uid, updated_order,
                                                                       context)

            return {
                'success': True,
                'order_total': rml_obj.formatLang(updated_order.amount_total, digits=price_digits),
                'order_subtotal': rml_obj.formatLang(updated_order.amount_subtotal,
                                                     digits=price_digits),
                'order_total_taxes': rml_obj.formatLang(updated_order.amount_tax,
                                                        digits=price_digits),
                'order_total_tax_overview': tax_overview,
                'order_total_delivery': rml_obj.formatLang(updated_order.carrier_id.normal_price,
                                                           digits=price_digits)
            }
        else:
            return {'success': False}

    @http.route(['/shop/checkout/change_delivery'], type='json', auth="public", website=True,
                multilang=True)
    def change_delivery(self, **post):
        """
        If delivery method is was changed in frontend change and apply delivery
        carrier / amount to sale order.
        """
        cr, uid, context = request.cr, request.uid, request.context
        order = request.website.sale_get_order()
        carrier_id = int(post.get('carrier_id'))

        return self.do_change_delivery(cr, uid, order, carrier_id, context=context)

    @http.route()
    def cart(self, **post):
        """
        If one active delivery carrier exists apply this delivery to sale order.
        """
        cr, uid, context = request.cr, request.uid, request.context

        response_object = super(website_sale, self).cart(**post)
        values = response_object.qcontext

        dc_ids = request.registry.get('delivery.carrier').search(
            cr, uid, [('active', '=', True), ('website_published', '=', True)])
        change_delivery = True
        if dc_ids and len(dc_ids) == 1:
            for line in values['order'].order_line:
                if line.is_delivery:
                    change_delivery = False
                    break
            if change_delivery:
                self.do_change_delivery(cr, uid, values['order'], dc_ids[0], context=context)

        return request.website.render(response_object.template, values)

    @http.route(['/page/terms_and_conditions/'], type='http', auth="public", website=True,
                multilang=True)
    def checkout_terms(self, **opt):
        """
        """
        return request.website.render('website_sale_osc.checkout_terms')

    @http.route('/shop/get_country', type='json', auth="public", website=True, multilang=True)
    def get_country(self, **post):
        """
        AJAX call in zippopotam module.
        """
        cr, uid, context, registry, website = request.cr, request.uid, request.context, \
                                              request.registry, request.website

        orm_country = registry.get('res.country')

        # get countries dependent on website settings
        country_ids = []
        if website.use_all_checkout_countries:
            country_ids = orm_country.search(cr, SUPERUSER_ID, [], context=context)
        else:
            country_ids = orm_country.search(
                cr, SUPERUSER_ID, [('id', 'in', [c.id for c in website.checkout_country_ids])],
                context=context)

        countries = {}
        for state in orm_country.browse(cr, uid, country_ids, context):
            countries.update({state.id: state.name})

        return countries

    @http.route('/shop/get_related_state', type='json', auth='public', website=True)
    def get_state(self, **post):
        """
        Overwrites module: website_sale.

        Returns states related to one country. If no states exist for one
        country an empty list will be returned.
        """
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        states = {}
        state_orm = registry.get('res.country.state')
        if 'country_id' in post and not post['country_id'] == '':
            states_ids = state_orm.search(cr, uid, [('country_id', '=', int(post['country_id']))],
                                          context=context)
            for state in state_orm.browse(cr, uid, states_ids, context):
                states.update({state.id: state.name})

        return states
