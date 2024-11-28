# Copyright 2024 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import http, models

logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _serve_page(cls):
        response = super()._serve_page()

        if not response and getattr(response, "status_code", 0) != 200:
            return response

        if (
            http.request.db
            and http.request.session.uid
            and http.request.env.user.has_group("website.group_website_designer")
        ):
            return response

        page = (
            http.request.env["website.page"]
            .sudo()
            .search(
                [("url", "=", http.request.httprequest.path)],
                order="website_id asc",
                limit=1,
            )
        )
        if not page:  # pragma: no cover
            logger.error("Served page found for URL %s", http.request.httprequest.path)
            return response

        if not page.is_redirect or page.redirect_method != "http":
            return response

        return http.request.redirect(
            page.redirect_url,
            code=int(page.redirect_http_code) if page.redirect_http_code else 301,
            local=not page.redirect_url.lower().startswith("http"),
        )
