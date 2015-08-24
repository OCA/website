# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    membership_prorrate = fields.Boolean(
        string="Prorrate",
        help="If this check is marked, then the fee will be proportionally "
             "charged for the remaining time of the period")
