###############################################################################
# For copyright and license notices, see __manifest__.py file in root directory
###############################################################################
from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

try:
    from odoo.addons.sale.controllers.portal import CustomerPortal
except ImportError:
    CustomerPortal = object


class CustomerPortal(CustomerPortal):
    @http.route(
        ["/my/order/duplicate/<int:order>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_order_duplicate(self, order, access_token=None):
        try:
            order_sudo = self._document_check_access(
                "sale.order", order, access_token=access_token
            )
        except AccessError:
            return request.redirect("/my")
        order_copy = order_sudo.copy()
        request.session["sale_order_id"] = order_copy.id
        return request.redirect("/shop/cart")
