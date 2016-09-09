# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from openerp.http import request, route
from openerp.exceptions import AccessError
from openerp.addons.website_portal_v10.controllers.main import WebsiteAccount


class PortalPurchaseWebsiteAccount(WebsiteAccount):
    def _purchase_order_domain(self, quotation):
        """Generate a domain for ``purchase.order`` objects.

        :param bool quotation:
            Set to ``True`` if you want quotation, ``False`` if you want
            purchase orders.
        """
        return [
            ("message_partner_ids", "child_of",
             request.env.user.partner_id.commercial_partner_id.ids),
            ("state", "in",
             ("sent", "cancel", "to approve") if quotation
             else ("purchase", "done")),
        ]

    def _prepare_purchase_orders_values(self, quotation, page=1,
                                        date_begin=None, date_end=None):
        """Get the render values for this ``purchase.order`` object."""
        values = self._prepare_portal_layout_values()
        PurchaseOrder = request.env["purchase.order"]
        url = "/my/purchase/{}".format("quotes" if quotation else "orders")

        # Get the domain for this view
        domain = self._purchase_order_domain(quotation)
        archive_groups = self._get_archive_groups("purchase.order", domain)
        if date_begin and date_end:
            domain += [("create_date", ">=", date_begin),
                       ("create_date", "<", date_end)]

        # Count for pager
        count = PurchaseOrder.search_count(domain)

        # Make pager
        pager = request.website.pager(
            url=url,
            url_args={"date_begin": date_begin, "date_end": date_end},
            total=count,
            page=page,
            step=self._items_per_page,
        )

        # Sarch the count to display, according to the pager data
        orders = PurchaseOrder.search(
            domain, limit=self._items_per_page, offset=pager["offset"])

        values.update({
            "date": date_begin,
            "orders": orders,
            "pager": pager,
            "archive_groups": archive_groups,
            "default_url": url,
        })

        return values

    @route()
    def account(self):
        """Add purchases documents to main account page."""
        response = super(PortalPurchaseWebsiteAccount, self).account()

        try:
            PurchaseOrder = request.env["purchase.order"]
            response.qcontext.update({
                "supplier_quotation_count": PurchaseOrder.search_count(
                    self._purchase_order_domain(True)),
                "supplier_order_count": PurchaseOrder.search_count(
                    self._purchase_order_domain(False)),
            })
        except AccessError:
            pass

        return response

    @route(["/my/purchase/quotes", "/my/purchase/quotes/page/<int:page>"],
           type="http", auth="user", website=True)
    def portal_my_purchase_quotes(self, page=1, date_begin=None, date_end=None,
                                  **kwargs):
        """List subscribed purchase quotes."""
        return request.website.render(
            "website_portal_purchase.portal_my_quotations",
            self._prepare_purchase_orders_values(
                True, page, date_begin, date_end))

    @route(["/my/purchase/orders", "/my/purchase/orders/page/<int:page>"],
           type="http", auth="user", website=True)
    def portal_my_purchase_orders(self, page=1, date_begin=None, date_end=None,
                                  **kwargs):
        """List subscribed purchase orders."""
        return request.website.render(
            "website_portal_purchase.portal_my_orders",
            self._prepare_purchase_orders_values(
                False, page, date_begin, date_end))

    @route(["/my/purchase/orders/<model('purchase.order'):order>"],
           type="http", auth="user", website=True)
    def purchase_orders_followup(self, order=None, **kw):
        order_invoice_lines = {
            il.product_id.id: il.invoice_id
            for il in order.invoice_ids.mapped("invoice_line_ids")}
        return request.website.render(
            "website_portal_purchase.orders_followup",
            {
                "order": order.sudo(),
                "order_invoice_lines": order_invoice_lines,
            })
