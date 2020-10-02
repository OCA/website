# Copyright 2020 Commown SCIC SAS (https://commown.fr)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def sale_get_order(self, force_create=False, code=None,
                       update_pricelist=False, force_pricelist=False):
        sale_order = super(Website, self).sale_get_order(
            force_create=force_create, code=code,
            update_pricelist=update_pricelist, force_pricelist=force_pricelist)
        if sale_order:
            if code:
                if sale_order.coupon_code and sale_order.coupon_code != code:
                    sale_order.clear_promotions()
                if not sale_order.coupon_code:
                    sale_order.add_coupon(code)
            elif code is not None:
                sale_order.clear_promotions()
            if code or sale_order.coupon_code:
                sale_order.apply_promotions()
        return sale_order
