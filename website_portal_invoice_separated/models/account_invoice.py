# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        """Handle mocked searches."""
        type_ = self.env.context.get("force_invoice_type")
        if type_:
            args.append(("type", "in", ["{}_{}".format(type_, kind)
                                        for kind in ("invoice", "refund")]))
        return super(AccountInvoice, self).search(
            args, offset, limit, order, count=count)
