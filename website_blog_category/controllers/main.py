# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import http
from odoo.addons.website.models.website import unslug
from odoo.addons.website_blog.controllers.main import WebsiteBlog


route = '/blog/<model("blog.blog"):blog>/category/<string:category>'


class WebsiteBlog(WebsiteBlog):

    @http.route([
        route,
        '%s/page/<int:page>' % route,
    ], type='http', auth="public", website=True)
    def blog_categories(self, blog=None, category=None, page=1, **opt):
        """ It filters out blog posts not of correct category """
        context = http.request.env.context.copy()
        category = http.request.env['blog.category'].browse(
            unslug(category)[1],
        )
        context.update({
            'website_category_id': category.id,
        })
        http.request.env.context = context
        res = self.blog(blog, None, page, **opt)
        res.qcontext.update({
            'category': category,
        })
        return res
