from openerp import http
from openerp.http import request
import openerp.addons.website_sale.controllers.main


class website_sale(openerp.addons.website_sale.controllers.main.website_sale):

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        order = request.website.sale_get_order()
        if order:
            from_currency = pool.get('product.price.type')._get_field_currency(cr, uid, 'list_price', context)
            to_currency = order.pricelist_id.currency_id
            compute_currency = lambda price: pool['res.currency']._compute(cr, uid, from_currency, to_currency, price, context=context)
        else:
            compute_currency = lambda price: price

        values = {
            'website_sale_order': order,
            'compute_currency': compute_currency,
            'suggested_products': [],
        }
        if order:
            _order = order
            if not context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()

        if post.get('type') == 'popover':
            return request.website.render(
                "website_sale_cart_preview.cart_popover", values)

        return request.website.render("website_sale.cart", values)
