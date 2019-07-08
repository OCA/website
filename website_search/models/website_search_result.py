# -*- coding: utf-8 -*-
# Copyright 2017-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring
import re
from collections import defaultdict
from odoo import fields, models
from odoo.tools import html2plaintext

PREVIEW_LEN = 60


class WebsiteSearchResult(models.TransientModel):
    _name = "website.search.result"
    _description = "Website Search Result"
    _order = "rank desc"

    name = fields.Char()
    preview = fields.Html()
    link = fields.Char()
    search_id = fields.Many2one("website.search", required=True)
    res_model = fields.Char()
    res_id = fields.Integer()
    rank = fields.Float()
    type = fields.Selection([("page", "Page")], required=True)

    def _compute_lazy(self):
        """As generating previews can be expensive, we lazily generate them
        when a result is shown in case they're not prefilled.

        Declare a method calls _compute_lazy_YOUR_TYPE to use this
        mechanism."""
        by_type = defaultdict(lambda: self)
        for this in self:
            if this.preview is not False:
                continue
            by_type[this.type] += this
        for result_type, results in by_type.items():
            compute_function = getattr(
                self,
                "_compute_lazy_%s" % result_type,
                None,
            )
            if not compute_function:
                continue
            compute_function.__func__(results)

    def _compute_lazy_page(self):
        for this in self:
            view = self.env[this.res_model].browse(this.res_id)
            # TODO: don't fully render this, pass a qweb engine that doesn't
            # resolve the main template. We'll probably want to cache this too
            htmlcontent = str(view.render(engine="website.search.qweb.engine"))

            # TODO: delete this when the above is done
            htmlcontent = (
                htmlcontent.split("<main>")[1]
                .split("<main>")[0]
                .strip()
                .replace("\\n", "")
            )
            # TODO: parse the doc and generate the preview on element level
            txtcontent = html2plaintext(htmlcontent).replace("\n", " ")
            firstmatch = re.search(
                this.search_id.name,
                txtcontent,
                re.IGNORECASE,
            )
            preview = view.name or view.key
            if firstmatch:
                if len(txtcontent) > PREVIEW_LEN:
                    start = max(0, firstmatch.start() - PREVIEW_LEN / 2)
                    end = min(len(txtcontent), firstmatch.end() + PREVIEW_LEN / 2)
                    preview = "..." + txtcontent[start:end] + "..."
                else:
                    preview = txtcontent
            this.write({"preview": preview})
