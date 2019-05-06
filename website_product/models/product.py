# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template',
                'website.seo.metadata']

    website_description = fields.Html(
        'Description for the website', sanitize_attributes=False,
        translate=html_translate, )

    website_product_url = fields.Char(
        'Website Product URL', compute='_compute_website_product_url')

    website_product_published = fields.Boolean(
        'Available on the Website catalogue', copy=False)

    @api.multi
    def _compute_website_product_url(self):
        for product in self:
            product.website_product_url = "/catalog/product/%s" % slug(product)

    @api.multi
    def website_product_publish_button(self):
        self.ensure_one()
        if self.env.user.has_group(
                'website.group_website_publisher'):
            return self.open_website_product_url()
        return self.write(
            {'website_published': not self.website_product_published})

    def open_website_product_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': self.website_product_url,
            'target': 'self',
        }


class ProductProduct(models.Model):
    _inherit = 'product.product'
    _inherits = {'product.template': 'product_tmpl_id'}
