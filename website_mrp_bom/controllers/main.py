# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import http
from odoo.http import request


class WebsiteMrpBomPage(http.Controller):

    @http.route(['/components/<model("mrp.bom"):bom>'], type='http',
                auth="public", website=True)
    def boms_detail(self, bom=False, **post):
        if bom and (
                bom.website_published or self._is_website_publisher(request)):
            values = {
                'main_object': bom,
                'bom': bom,
                'has_published_bom': self._has_published_bom(bom)
            }
            return request.render("website_mrp_bom.mrp_bom_page", values)
        return request.not_found()

    @staticmethod
    def _is_website_publisher(req):
        return req.env.user.has_group('website.group_website_publisher')

    @staticmethod
    def _has_published_bom(bom):
        has_published_bom = False
        for bom_line in bom.bom_line_ids:
            if bom_line.product_id.sudo().bom_ids:
                if bom_line.product_id.sudo().bom_ids[0].website_published:
                    has_published_bom = True
                    break
        return has_published_bom
