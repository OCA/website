# -*- coding: utf-8 -*-
# Copyright 2019 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _set_public_user_pricelist(self):
        """Make sure public user has a pricelist to prevent test failures."""
        public_user = self.env.ref('base.public_user')
        pricelist = self.env.ref('product.list0')
        public_user.write({'property_product_pricelist': pricelist.id})
