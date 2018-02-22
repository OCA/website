# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp.addons.website_portal_sale_v10.controllers.main import \
    WebsiteAccount as PortalSaleWebsiteAccount
from openerp.addons.website_portal_purchase.controllers.main import \
    PortalPurchaseWebsiteAccount
from openerp.http import route, request
from functools import wraps


def invoice_type(type_):
    """Decorator to filter invoices by type.

    :param str type_:
        It can be either ``in`` or ``out``, depending on the invoice types
        you want.
    """
    def superwrapper(wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            # Modify request's env
            old_context = request.context.copy()
            request.context["force_invoice_type"] = type_
            del request.env

            # Get modified result
            result = wrapped(*args, **kwargs)

            # Restore request's env
            request.context = old_context
            del request.env

            return result
        return wrapper
    return superwrapper


class WebsiteAccount(PortalSaleWebsiteAccount, PortalPurchaseWebsiteAccount):
    @route()
    def account(self):
        """Separate customer and supplier invoices."""
        response = (invoice_type("out")
                    (super(WebsiteAccount, self).account)())

        # Check visitor has supplier permissions
        if "supplier_order_count" in response.qcontext:
            response.qcontext["supplier_invoice_count"] = (
                request.env["account.invoice"].search_count([
                    ("message_partner_ids", "child_of",
                     request.env.user.commercial_partner_id.ids),
                    ("state", "in", ("open", "paid", "cancelled")),
                    ("type", "in", ("in_invoice", "in_refund")),
                ]))

        return response

    @route()
    @invoice_type("out")
    def portal_my_invoices(self, *args, **kwargs):
        """Decorator does all the work."""
        return super(WebsiteAccount, self).portal_my_invoices(*args, **kwargs)

    @route(['/my/purchase/invoices', '/my/purchase/invoices/page/<int:page>'],
           type='http', auth="user", website=True)
    @invoice_type("in")
    def portal_my_purchase_invoices(self, *args, **kwargs):
        """Purchase invoices list."""
        qcontext = super(WebsiteAccount, self).portal_my_invoices(
            *args, **kwargs).qcontext
        qcontext["default_url"] = "/my/purchase/invoices"
        return request.website.render(
            "website_portal_invoice_separated.portal_my_purchase_invoices",
            qcontext)
