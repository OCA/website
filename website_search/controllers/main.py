# -*- coding: utf-8 -*-
# Copyright 2019 - Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class GlobalSearch(Website):
    @http.route(
        [
            "/search",
            "/search/<int:search_id>",
            "/search/<int:search_id>/page/<int:page>",
        ],
        type="http",
        auth="public",
        csrf=False,
        website=True,
    )
    def search(self, page=1, search_id=None, **kwargs):
        # pick up results from existing search
        search = request.env["website.search"].browse(search_id or [])
        # or create a new search
        if kwargs.get("name"):
            search = request.env["website.search"].create(kwargs)
            search._do_search()
        step = request.env["ir.config_parameter"].get_param(
            "website_search.results_per_page",
            10,
        )
        pager = request.website.pager(
            url="/search/%s" % search.id,
            # we get back our search text for page 2,3...
            total=len(search.result_ids),
            page=page,
            step=step,
        )
        return request.render(
            "website_search.results",
            {
                "search": search,
                "pager": pager,
                "step": step,
            },
        )
