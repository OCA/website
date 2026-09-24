# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website as WebsiteController


class Website(WebsiteController):
    DEFAULT_LIMIT = 10
    MAX_LIMIT = 100

    @http.route(
        "/website/field_autocomplete/<string:model>",
        type="jsonrpc",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def _get_field_autocomplete(self, model, **kwargs):
        """Return JSON autocomplete data."""
        domain = kwargs.get("domain") or []
        fields = kwargs.get("fields") or []
        limit = kwargs.get("limit")
        records = self._fetch_autocomplete_data(model, domain, fields, limit)
        return list(records.values())

    def _fetch_autocomplete_data(self, model, domain, fields, limit=None):
        """Return readable records for a website field autocomplete."""
        if (
            not isinstance(domain, list)
            or not isinstance(fields, list)
            or not fields
            or not all(isinstance(field, str) and field for field in fields)
        ):
            return {}

        try:
            limit = int(limit or self.DEFAULT_LIMIT)
        except (TypeError, ValueError):
            limit = self.DEFAULT_LIMIT
        limit = min(max(limit, 1), self.MAX_LIMIT)

        records = (
            request.env[model]
            .with_user(request.website.user_id.id)
            .search_read(domain, fields, limit=limit)
        )
        return {record["id"]: record for record in records}
