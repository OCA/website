# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.portal.controllers import portal

DEFAULT_LIMIT_OPTIONS = [10, 20, 40, 80, 100]
OPTIONS_PARAM = "website_portal_pager_limit.options"


class CustomerPortal(portal.CustomerPortal):
    # Defined as a property so that every portal route relying on
    # ``self._items_per_page`` (sale, account, project, ...) transparently
    # honors the ``limit`` query parameter without overriding each route.
    @property
    def _items_per_page(self):
        limit = request.httprequest.args.get("limit", "")
        if limit.isdigit() and int(limit) in self._get_portal_pager_limit_options():
            return int(limit)
        # Invalid or missing value: fall back to the standard portal page size
        return portal.CustomerPortal._items_per_page

    def _get_portal_pager_limit_options(self):
        """Return the whitelist of allowed page sizes.

        Misconfigured values (non digits, empty string) are discarded so a
        broken system parameter can never disable the portal pagination.
        """
        param = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param(OPTIONS_PARAM, default="10,20,40,80,100")
        )
        options = [int(x.strip()) for x in param.split(",") if x.strip().isdigit()]
        return options or list(DEFAULT_LIMIT_OPTIONS)

    def _prepare_portal_layout_values(self):
        values = super()._prepare_portal_layout_values()
        values.update(
            portal_pager_limit_options=self._get_portal_pager_limit_options(),
            portal_pager_limit=self._items_per_page,
        )
        return values
