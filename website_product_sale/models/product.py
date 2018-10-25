# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, models
from odoo.addons.http_routing.models.ir_http import slug


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _compute_website_url(self):
        # If the product cannot be sold, use website_product view.
        # Otherwise, use the default URL from website_sale, which will
        # redirect the user to the shop.
        super(ProductTemplate, self)._compute_website_url()
        for product in self:
            if not product.sale_ok:
                product.website_url = "/product/%s" % slug(product)
