# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request


class ShopUserOrdersController(http.Controller):
    """ This is mainly a porting of `website_sale`
    orders_followup controller from v9 master.
    """

    orders_followup_template = "website_sale_customer.orders_followup"

    @http.route([
        '/shop/orders',
        '/shop/orders/page/<int:page>',
    ], type='http', auth="user", website=True)
    def orders_followup(self, page=1, by=5, **post):
        partner = request.env['res.users'].browse(request.uid).partner_id
        orders = request.env['sale.order'].sudo().search(
            [('partner_id', '=', partner.id),
             ('state', 'not in', ['draft', 'cancel'])])

        nbr_pages = max((len(orders) / by) +
                        (1 if len(orders) % by > 0 else 0), 1)
        page = min(page, nbr_pages)
        pager = request.website.pager(
            url='/shop/orders', total=nbr_pages, page=page, step=1,
            scope=by, url_args=post
        )
        orders = orders[by * (page - 1): by * (page - 1) + by]

        order_invoice_lines = {}
        for o in orders:
            invoiced_lines = request.env['account.invoice.line'].sudo().search(
                [('invoice_id', 'in', o.invoice_ids.ids)])
            order_invoice_lines[o.id] = {
                il.product_id.id: il.invoice_id
                for il in invoiced_lines
            }

        return request.website.render(self.orders_followup_template, {
            'orders': orders,
            'order_invoice_lines': order_invoice_lines,
            'pager': pager,
        })
