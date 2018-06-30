# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.http import request


class BlogMap(http.Controller):
    @http.route(
        '/blogmap/<model("blog.blog"):blog>', type='http', auth="public",
        website=True,
    )
    def blogmap(self, blog):
        return self._generic_map(
            request.env['ir.model'].search([('model', '=', 'blog.post')]),
            domain=[('blog_id', '=', blog.id)],
        )

    def _generic_map(self, model, domain=None, options=None):
        return request.website.render(
            "website_blog_location.base_location_map",
            values={
                'records': request.env[model.model].search(
                    domain or []
                ),
            },
        )
