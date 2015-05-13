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
from openerp import SUPERUSER_ID
from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.report import report_sxw


class website_sale(website_sale):

    """Add aditional functions to the website_sale controller."""

    mandatory_billing_fields = ["name", "phone", "email", "street", "city", "country_id", "zip"]
    optional_billing_fields = ["street2", "state_id", "vat", "vat_subjected"]

    @http.route(['/shop/checkout'], type='http', auth='public', website=True, multilang=True)
    def checkout(self, **post):
        """Checkout controller."""
        # if onestepcheckout is deactivated use the normal checkout
        if not request.website.use_osc:
            return super(website_sale, self).checkout()

        website = request.website

        # must have a draft sale order with lines at this point, otherwise reset
        order = request.website.sale_get_order()

        redirection = self.checkout_redirection(order)
        if redirection:
            return redirection

        values = self.checkout_values(post)

        # get countries dependent on website settings
        orm_country = request.env['res.country']
        orm_user = request.env['res.users']
        partner = orm_user.sudo().browse(request.uid).partner_id

        if website.use_all_checkout_countries:
            countries = orm_country.search([])
        else:
            countries = orm_country.search(
                [('id', 'in', [c.id for c in website.checkout_country_ids])])
        values['countries'] = countries

        if not post:
            if request.uid != request.website.user_id.id:
                values['checkout'].update({'street': partner.street_name,
                                           'street_number': partner.street_number})

        result = self.payment(post=post)
        values.update(result.qcontext)

        # get additional tax information
        values['tax_overview'] = request.env['sale.order'].tax_overview(order)
        return request.website.render('website_sale_osc.osc_onestepcheckout', values)

    @http.route(['/shop/checkout/confirm_address/'], type='json', auth='public', website=True,
                multilang=True)
    def confirm_address(self, **post):
        """Address controller."""
        # must have a draft sale order with lines at this point, otherwise redirect to shop
        order = request.website.sale_get_order()
        if not order or order.state != 'draft' or not order.order_line:
            request.session['sale_order_id'] = None
            request.session['sale_transaction_id'] = None
            return request.redirect('/shop')
        # if transaction pending / done: redirect to confirmation
        tx = request.context.get('website_sale_transaction')
        if tx and tx.state != 'draft':
            return request.redirect('/shop/payment/confirmation/%s' % order.id)

        orm_partner = request.env['res.partner']
        orm_user = request.env['res.users']
        orm_country = request.env['res.country']
        countries = orm_country.sudo().search([])
        orm_state = request.env['res.country.state']
        states = orm_state.sudo().search([])

        info = {}
        values = {
            'countries': countries,
            'states': states,
            'checkout': info,
            'shipping': post.get('shipping_different')
        }
        checkout = values['checkout']
        checkout.update(post)

        values['error'] = self.checkout_form_validate(values['checkout'])
        if values['error']:
            return {
                'success': False,
                'errors': values['error']
            }

        company_name = ''
        if 'company' in checkout:
            company_name = checkout['company']
        company = None

        if 'company' in post and post['company']:
            companies = orm_partner.sudo().search([('name', 'ilike', company_name),
                                                   ('is_company', '=', True)])
            company = (companies and companies[0]) or orm_partner.sudo().create({
                'name': company_name,
                'is_company': True
            })

        checkout['street_name'] = checkout.get('street')
        if checkout.get('street_number'):
            checkout['street'] = checkout.get('street') + ' ' + checkout.get('street_number')

        billing_info = dict((k, v) for k, v in checkout.items() if 'shipping_' not in k and k !=
                            'company')
        billing_info['parent_id'] = (company and company.id) or None
        partner = None

        if request.uid != request.website.user_id.id:
            partner = orm_user.sudo().browse(request.uid).partner_id
        elif order.partner_id:
            domain = [('active', '=', False), ('partner_id', '=', order.partner_id.id)]
            users = request.env['res.users'].sudo().search(domain)
            if not users or request.website.user_id.id not in users.ids:
                partner = order.partner_id

        if partner:
            partner.sudo().write(billing_info)
        else:
            partner = orm_partner.sudo().create(billing_info)
        shipping_partner_id = None
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
                'parent_id': partner.id,
                'country_id': post['shipping_country_id'],
                'state_id': post['shipping_state_id'],
            }
            domain = [(key, '_id' in key and '=' or 'ilike', '_id' in key and value and int(
                value) or value)
                for key, value in shipping_info.items() if key in
                self.mandatory_billing_fields + ['type', 'parent_id']]
            shipping_partners = orm_partner.sudo().search(domain)
            if shipping_partners:
                shipping_partner_id = shipping_partners[0].id
                orm_partner.write([shipping_partner_id], shipping_info)
            else:
                shipping_partner_id = orm_partner.sudo().create(shipping_info).id

        order_info = {
            'partner_id': partner.id,
            'message_follower_ids': [(4, partner.id), (3, request.website.partner_id.id)],
            'partner_invoice_id': partner.id
        }
        order_info.update(request.env['sale.order'].sudo().onchange_partner_id(
            partner.id)['value'])
        # we need to update partner_shipping_id after onchange_partner_id() call
        # otherwise the deselection of the option 'Ship to a different address'
        # would be overwritten by an existing shipping partner type
        order_info.update({'partner_shipping_id': shipping_partner_id or partner.id})
        order_info.pop('user_id')

        order.sudo().write(order_info)
        request.session['sale_last_order_id'] = order.id
        return {'success': True}

    def do_change_delivery(self, order, carrier_id):
        """Apply delivery amount to current sale order."""
        if order and carrier_id:

            # order_id is needed to get delivery carrier price
            if not request.context.get('order_id'):
                request.context['order_id'] = order.id

            # recompute delivery costs
            request.env['sale.order']._check_carrier_quotation(order, force_carrier_id=carrier_id)

            # generate updated total prices
            updated_order = request.website.sale_get_order()
            product_pool = request.env['product.product']
            rml_obj = report_sxw.rml_parse(request.cr, SUPERUSER_ID, product_pool._name,
                                           context=request.context)
            price_digits = rml_obj.get_digits(dp='Product Price')

            # get additional tax information
            tax_overview = request.env['sale.order'].tax_overview(updated_order)

            return {
                'success': True,
                'order_total': rml_obj.formatLang(updated_order.amount_total, digits=price_digits),
                'order_subtotal': rml_obj.formatLang(updated_order.amount_subtotal,
                                                     digits=price_digits),
                'order_total_taxes': rml_obj.formatLang(updated_order.amount_tax,
                                                        digits=price_digits),
                'order_total_tax_overview': tax_overview,
                'order_total_delivery': rml_obj.formatLang(updated_order.amount_delivery,
                                                           digits=price_digits)
            }
        else:
            return {'success': False}

    @http.route(['/shop/checkout/change_delivery'], type='json', auth="public", website=True,
                multilang=True)
    def change_delivery(self, **post):
        """
        If delivery method is was changed in frontend.

        Change and apply delivery carrier / amount to sale order.
        """
        order = request.website.sale_get_order()
        carrier_id = int(post.get('carrier_id'))

        return self.do_change_delivery(order, carrier_id)

    @http.route()
    def cart(self, **post):
        """If one active delivery carrier exists apply this delivery to sale order."""
        response_object = super(website_sale, self).cart(**post)
        values = response_object.qcontext

        dc_ids = request.env['delivery.carrier'].search(
            [('active', '=', True), ('website_published', '=', True)])
        change_delivery = True
        if dc_ids and len(dc_ids) == 1:
            for line in values['order'].order_line:
                if line.is_delivery:
                    change_delivery = False
                    break
            if change_delivery:
                self.do_change_delivery(values['order'], dc_ids[0])

        return request.website.render(response_object.template, values)

    @http.route(['/page/terms_and_conditions/'], type='http', auth="public", website=True,
                multilang=True)
    def checkout_terms(self, **opt):
        """Function for terms of condition."""
        return request.website.render('website_sale_osc.checkout_terms')
