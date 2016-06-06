# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import api, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def check_access_rule(self, operation):
        """Bypass exception in some contexts."""
        try:
            return super(ProductTemplate, self).check_access_rule(operation)
        except:
            if self.env.context.get("no_access_error"):
                return False
            raise
