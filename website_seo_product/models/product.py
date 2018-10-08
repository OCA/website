# -*- coding: utf-8 -*-
# Copyright 2018 Wolfgang Pichler, Callino <wpichler@callino.at>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.addons.website.models.website import slug


class ProductTemplate(models.Model):
    _inherit = ["product.template"]

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if 'name' not in vals:
            return result
        for product in self:
            redirection = self.env['website.seo.redirection'].search(
                [('origin', '=', "/shop/product/%s" % slug(product))])
            if redirection:
                redirection.origin = "/shop/product/%s" %\
                                     slug((product.id, vals['name']))
        return result

    @api.multi
    def _compute_website_url(self):
        super(ProductTemplate, self)._compute_website_url()
        for product in self:
            redirection = self.env['website.seo.redirection'].search([
                ('origin', '=', "/shop/product/%s" % slug(product))
            ])
            if redirection:
                product.website_url = redirection.destination
            else:
                product.website_url = "/shop/product/%s" % slug(product)
