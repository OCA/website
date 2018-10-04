# -*- coding: utf-8 -*-
# Copyright 2018 Wolfgang Pichler, Callino <wpichler@callino.at>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.addons.website.models.website import slug


class ProductPublicCategory(models.Model):
    _inherit = [
        "product.public.category", 
        "website.seo.metadata", 
        "website.published.mixin"
    ]
    _name = 'product.public.category'

    def write(self, vals):
        result = super(ProductPublicCategory, self).write(vals)
        if 'name' not in vals:
            return result
        for public_category in self:
            redirection = self.env['website.seo.redirection'].search(
                [('origin', '=', "/shop/category/%s" %
                  slug(public_category))])
            if redirection:
                redirection.origin = "/shop/category/%s" %\
                                     slug((public_category.id, vals['name']))
        return result

    @api.multi
    def _compute_website_url(self):
        super(ProductPublicCategory, self)._compute_website_url()
        for public_category in self:
            redirection = self.env['website.seo.redirection'].search(
                [('origin', '=', "/shop/category/%s" %
                  slug(public_category))])
            if redirection:
                public_category.website_url = redirection.destination
            else:
                public_category.website_url = "/shop/category/%s"\
                                              % slug(public_category)
