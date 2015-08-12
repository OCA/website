# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def check_membership_expiry(self):
        """Force a recalculation on each partner that is member."""
        partners = self.search(
            [('membership_state', 'not in', ['old', 'none'])])
        # It has to be triggered one by one to avoid an error
        for partner in partners:
            partner.write({'membership_state': 'none'})
        return True
