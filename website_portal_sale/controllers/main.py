# -*- coding: utf-8 -*-

import datetime

from openerp import http
from openerp.http import request

from openerp.addons.website_portal.controllers.main import WebsiteAccount


class PortalSaleWebsiteAccount(WebsiteAccount):

    def _prepare_quotations(self, **kw):
        quotations = request.env['sale.order'].search([
            ('state', 'in', ['sent', 'cancel']),
        ])
        return quotations

    @http.route(
        ['/my/home/quotations'], type='http', auth="user", website=True)
    def quotations(self, **kw):
        quotations = {'quotations': self._prepare_quotations()}
        return request.website.render(
            'website_portal_sale.quotations_only', quotations)

    def _prepare_orders(self, **kw):
        orders = request.env['sale.order'].search([
            ('state', 'in', ['progress', 'manual', 'shipping_except',
                             'invoice_except', 'done'])
        ])
        return orders

    @http.route(['/my/home/orders'], type='http', auth="user", website=True)
    def orders(self, **kw):
        values = {'orders':  self._prepare_orders()}
        return request.website.render(
            'website_portal_sale.sale_orders_only', values)

    def _prepare_invoices(self, **kw):
        invoices = request.env['account.invoice'].search([
            ('state', 'in', ['open', 'paid', 'cancelled'])
        ])
        return invoices

    @http.route(['/my/home/invoices'], type='http', auth="user", website=True)
    def invoices(self, **kw):
        invoices = {'invoices': self._prepare_invoices()}
        return request.website.render(
            'website_portal_sale.invoices_only', invoices)

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(PortalSaleWebsiteAccount, self).account(**kw)
        if not request.env.user.partner_id.customer:
            return response
        quotations = self._prepare_quotations()
        orders = self._prepare_orders()
        invoices = self._prepare_invoices()

        response.qcontext.update({
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'quotations': quotations,
            'orders': orders,
            'invoices': invoices,
        })
        return response

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="user",
                website=True)
    def orders_followup(self, order_id=None):
        domain = [
            ('state', 'not in', ['draft', 'cancel']),
            ('id', '=', order_id)
        ]
        order = request.env['sale.order'].search(domain)
        if not order:
            return request.website.render("website.404")
        invoiced_lines = request.env['account.invoice.line'].search([
            ('invoice_id', 'in', order.invoice_ids.ids)
        ])
        order_invoice_lines = {il.product_id.id: il.invoice_id
                               for il in invoiced_lines}
        contact = order.sudo().user_id.partner_id
        contact_dict = {
            'phone': contact.phone,
            'email': contact.email,
        }
        return request.website.render("website_portal_sale.orders_followup", {
            'order': order,
            'order_invoice_lines': order_invoice_lines,
            'contact': contact_dict,
        })
