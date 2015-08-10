# -*- coding: utf-8 -*-
# (c) 2015 Pedro M. Baeza
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields
import openerp.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = "product.template"

    initial_fee = fields.Selection(
        selection=[('none', 'No initial fee'),
                   ('fixed', 'Fixed amount'),
                   ('percentage', 'Percentage of the price')],
        default='none', string="Initial fee", required=True)
    fixed_fee = fields.Float(digits_compute=dp.get_precision('Product Price'))
    percentage_fee = fields.Float(digits=(12, 2), string="Perc. fee (%)")
