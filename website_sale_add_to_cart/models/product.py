# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    website_btn_addtocart_published = fields.Boolean(
        string='Button Add To Cart',
        copy=False,
        default=True)
