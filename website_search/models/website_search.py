# -*- coding: utf-8 -*-
# Copyright 2017-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring
import inspect
from odoo import api, fields, models


class WebsiteSearch(models.TransientModel):
    """
    website search model implements all the base search functions that will be
    needed by specific search results
    """

    _name = "website.search"
    _description = "Website Search"

    name = fields.Char()
    result_ids = fields.One2many("website.search.result", "search_id")

    @api.multi
    def _do_search(self):
        """Add a function _do_search_YOUR_NAME() to implement searching for
        another model. Also add your name in website.search.result#type to
        identify your type of search results.

        Take the search string from self.name, and add your results to
        self.result_ids"""
        for func in inspect.getmembers(
            self,
            lambda x: inspect.ismethod(x) and x.__name__.startswith("_do_search_"),
        ):
            func[1]()

    @api.multi
    def _do_search_ir_view_page(self):
        # specific search method for a type of resource
        # must create records of type website.search.result  and add them
        # to result_ids of this search.
        self.env.cr.execute(
            """select
                id from (
                    select
                           id, page, name,
                           lower (array_to_string(
                                xpath(
                                    '//*//text()', arch_db::xml), '\n'
                                )) as view_text
                    from ir_ui_view
                    where type='qweb' and page='t') as table_text
                where table_text.view_text ilike %s or name ilike %s""",
            (
                "%" + (self.name or "") + "%",
                "%" + (self.name or "") + "%",
            ),
        )
        ids = [_id for _id, in self.env.cr.fetchall()]

        for view in self.env["ir.ui.view"].search([("id", "in", ids)]):
            self.env["website.search.result"].create(
                {
                    "res_model": "ir.ui.view",
                    "search_id": self.id,
                    "type": "page",
                    "res_id": view.id,
                    "link": "/page/%s" % view.key,
                    "name": view.name or view.key,
                    # give higher rank if search text is in page title
                    "rank": 1 and self.name.lower() in view.name.lower() or 2,
                }
            )

    def _get_results(self, offset, limit):
        results = self.result_ids.sorted(key=lambda x: x.rank)[offset : offset + limit]
        results._compute_lazy()
        return results
