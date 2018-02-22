# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class Website(models.Model):
    _inherit = "website"

    @api.multi
    def pager(self, url, total, page=1, step=30, scope=5, url_args=None):
        """Mock URL in pager."""
        if (url == "/my/invoices" and
                self.env.context.get("force_invoice_type") == "in"):
            url = "/my/purchase/invoices"
        return super(Website, self).pager(
            url, total, page, step, scope, url_args)
