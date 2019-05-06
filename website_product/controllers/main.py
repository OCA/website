# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo import http
from odoo.http import request


class WebsiteProductPage(http.Controller):

    @http.route(['/catalog/product/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    def products_detail(self, product=False, **post):
        if product and (
                product.website_product_published or
                self._is_website_publisher(request)):
            values = {
                'main_object': product,
                'product': product,
                'controller': '/catalog/publish'
            }
            return request.render("website_product.product_page", values)
        return request.not_found()

    @http.route(['/catalog/publish'],
                type='json', auth="public", website=True)
    def publish(self, id, object):  # noqa
        Model = request.env[object]  # noqa
        record = Model.browse(int(id))  # noqa

        values = {}
        if 'website_product_published' in Model._fields:
            values['website_product_published'] = \
                not record.website_product_published
        record.write(values)
        return bool(record.website_product_published)

    @staticmethod
    def _is_website_publisher(req):
        return req.env.user.has_group('website.group_website_publisher')
