#  Copyright 2023 Simone Rubino - TAKOBI
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import re
from odoo import api, fields, models


class Website(models.Model):
    _inherit = 'website'

    forbidden_url_ids = fields.One2many(
        comodel_name="website.forbidden.url",
        inverse_name="website_id",
        string="Forbidden URLs regex",
    )

    @api.multi
    def enumerate_pages(self, query_string=None, force=False):
        pages = super().enumerate_pages(query_string=query_string, force=force)
        forbidden_url_regexes = self.mapped("forbidden_url_ids.regex")
        forbidden_url_compiled_regexes = list(map(re.compile, forbidden_url_regexes))
        for page in pages:
            is_forbidden = \
                self._is_enumerated_page_forbidden_by_regexes(
                    page, forbidden_url_compiled_regexes,
                )
            if not is_forbidden:
                yield page

    def _is_enumerated_page_forbidden_by_regexes(self, page, compiled_regexes):
        page_url = page["loc"]
        for forbidden_url_compiled_regex in compiled_regexes:
            is_url_forbidden = forbidden_url_compiled_regex.match(page_url)
            if is_url_forbidden:
                is_forbidden = True
                break
        else:
            is_forbidden = False
        return is_forbidden
