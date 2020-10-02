# Copyright 2020 Commown SCIC SAS (https://commown.fr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request
from odoo.addons.sale.controllers.product_configurator import (
    ProductConfiguratorController)


class WebsiteSale(ProductConfiguratorController):

    @http.route(["/shop/pricelist"], type="http", auth="public", website=True,
                sitemap=False)
    def pricelist(self, promo, **post):
        redirect = post.get("r", "/shop/cart")
        # empty promo code is used to reset/remove pricelist
        # (see `sale_get_order()`)
        if promo:
            promotion_rule = request.env["sale.promotion.rule"].sudo().search([
                ("code", "=", promo)], limit=1)
            if not promotion_rule:
                return request.redirect("%s?code_not_available=1" % redirect)

        request.website.sale_get_order(code=promo)
        return request.redirect(redirect)
