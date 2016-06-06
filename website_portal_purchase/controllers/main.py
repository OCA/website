# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import datetime

from openerp import http
from openerp.http import request

from openerp.addons.website_portal.controllers.main import WebsiteAccount


class PortalPurchaseWebsiteAccount(WebsiteAccount):

    def _prepare_request_quotations(self):
        quotations = request.env['purchase.order'].search([
            ('state', 'in', ['sent', 'bid', 'confirmed', 'cancel'])
        ])
        return quotations

    @http.route(
        ['/my/supplier/request-quotations'], type='http', auth="user",
        website=True)
    def request_quotations(self):
        quotations = {'request_quotations': self._prepare_request_quotations()}
        return request.website.render(
            'website_portal_purchase.request_quotations_only', quotations)

    def _prepare_purchase_orders(self):
        orders = request.env['purchase.order'].search([
            ('state', 'in', ['approved', 'except_picking',
                             'except_invoice', 'done'])
        ])
        return orders

    @http.route(['/my/supplier/orders'], type='http', auth="user",
                website=True)
    def supplier_orders(self):
        values = {'purchase_orders':  self._prepare_purchase_orders()}
        return request.website.render(
            'website_portal_purchase.purchase_orders_only', values)

    def _prepare_supplier_invoices(self):
        invoices = request.env['account.invoice'].search([
            ('state', 'in', ['open', 'paid', 'cancelled']),
            ('type', 'in', ['in_invoice', 'in_refund'])
        ])
        return invoices

    @http.route(
        ['/my/supplier/invoices'], type='http', auth="user", website=True)
    def supplier_invoices(self):
        invoices = {'supplier_invoices': self._prepare_supplier_invoices()}
        return request.website.render(
            'website_portal_purchase.invoices_only', invoices)

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def account(self, **kw):
        """ Add purchase documents to main account page """
        response = super(PortalPurchaseWebsiteAccount, self).account(**kw)
        if not request.env.user.partner_id.supplier:
            return response
        request_quotations = self._prepare_request_quotations()
        purchase_orders = self._prepare_purchase_orders()
        supplier_invoices = self._prepare_supplier_invoices()

        response.qcontext.update({
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'request_quotations': request_quotations,
            'purchase_orders': purchase_orders,
            'supplier_invoices': supplier_invoices,
        })
        return response

    @http.route(
        ['/my/supplier/orders/<int:order_id>'], type='http', auth="user",
        website=True)
    def supplier_orders_followup(self, order_id=None):
        domain = [
            ('state', 'not in', ['draft', 'cancel']),
            ('id', '=', order_id)
        ]
        order = request.env['purchase.order'].search(domain)
        invoiced_lines = request.env['account.invoice.line'].search([
            ('invoice_id', 'in', order.invoice_ids.ids)
        ])
        order_invoice_lines = {il.product_id.id: il.invoice_id
                               for il in invoiced_lines}
        return request.website.render(
            "website_portal_purchase.orders_followup",
            {
                'order': order,
                'order_invoice_lines': order_invoice_lines,
            })
