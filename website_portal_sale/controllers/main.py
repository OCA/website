# -*- coding: utf-8 -*-
import datetime

from openerp import http
from openerp.http import request

from openerp.addons.website_portal.controllers.main import website_account


class WebsiteAccount(website_account):

    @http.route(['/my/home'], type='http', auth="user", website=True)
    def account(self, **kw):
        """ Add sales documents to main account page """
        response = super(WebsiteAccount, self).account(**kw)

        partner = request.env.user.partner_id
        quotations = request.env['sale.order'].search([
            ('partner_id.id', '=', partner.id),
            ('state', 'in', ['sent', 'cancel'])
        ])
        orders = request.env['sale.order'].search([
            ('partner_id.id', '=', partner.id),
            ('state', 'in', ['progress', 'manual', 'shipping_except',
                             'invoice_except', 'done'])
        ])
        invoices = request.env['account.invoice'].search([
            ('partner_id.id', '=', partner.id),
            ('state', 'in', ['open', 'paid', 'cancelled'])
        ])

        response.qcontext.update({
            'date': datetime.date.today().strftime('%Y-%m-%d'),
            'quotations': quotations,
            'orders': orders,
            'invoices': invoices,
        })
        return response

    @http.route(['/my/orders/<int:order>'], type='http', auth="user",
                website=True)
    def orders_followup(self, order=None):
        partner = request.env['res.users'].browse(request.uid).partner_id
        domain = [
            ('partner_id.id', '=', partner.id),
            ('state', 'not in', ['draft', 'cancel']),
            ('id', '=', order)
        ]
        order = request.env['sale.order'].search(domain)
        invoiced_lines = request.env['account.invoice.line'].search([
            ('invoice_id', 'in', order.invoice_ids.ids)
        ])
        order_invoice_lines = {il.product_id.id: il.invoice_id
                               for il in invoiced_lines}

        return request.website.render("website_portal_sale.orders_followup", {
            'order': order.sudo(),
            'order_invoice_lines': order_invoice_lines,
        })
