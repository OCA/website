# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import api, fields, models
from odoo.addons.http_routing.models.ir_http import slug
from odoo.tools.translate import html_translate


class MrpBom(models.Model):
    _inherit = ["mrp.bom",
                "website.seo.metadata",
                'website.published.mixin']
    _name = 'mrp.bom'

    website_description = fields.Html('Description for the website',
                                      sanitize_attributes=False,
                                      translate=html_translate)

    @api.multi
    def _compute_website_url(self):
        for bom in self:
            bom.website_url = "/components/%s" % slug(bom)

    @api.multi
    def write(self, values):
        rec = super(MrpBom, self).write(values)
        if 'website_published' in values:
            pts = self.mapped('product_tmpl_id')
            pts.write(
                {'website_product_published': values['website_published']})
        return rec

    @api.multi
    def unlink(self):
        if self.website_published:
            pts = self.mapped('product_tmpl_id')
            pts.update({'website_product_published': False})
        return super(MrpBom, self).unlink()
