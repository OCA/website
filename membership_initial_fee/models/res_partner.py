# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def create_membership_invoice(self, product_id=None, datas=None):
        # This is a workaround for avoiding the overwriting of the invoice line
        # Part 1: pass a context variable - See
        # https://github.com/odoo/odoo/pull/7971
        obj = super(ResPartner,
                    self.with_context(create_membership_invoice=True))
        return obj.create_membership_invoice(
            product_id=product_id, datas=datas)
