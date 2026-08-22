# Copyright (C) 2026 XXP
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.http import request

from odoo.addons.portal.controllers import portal

DEFAULT_SIZE_OPTIONS = (10, 20, 40, 80, 100)
OPTIONS_PARAM = "portal_pager_size.options"


class CustomerPortal(portal.CustomerPortal):
    # Defined as a property so that every portal route relying on
    # ``self._items_per_page`` (sale, account, project, ...) transparently
    # honors the ``limit`` query parameter without overriding each route.
    @property
    def _items_per_page(self):
        """Resolve the active page size from the ``limit`` query parameter.

        The requested ``limit`` is honored only when it belongs to the
        configured whitelist; any invalid or missing value falls back to the
        standard portal page size, so pagination always stays functional.
        """
        limit = request.httprequest.args.get("limit", "")
        if limit.isdigit() and int(limit) in self._get_portal_pager_size_options():
            return int(limit)
        # Invalid or missing value: fall back to the standard portal page size
        return portal.CustomerPortal._items_per_page

    def _get_portal_pager_size_options(self):
        """Return the whitelist of allowed page sizes as a fresh ``list``.

        Misconfigured values (non digits, empty string) are discarded so a
        broken system parameter can never disable the portal pagination. A new
        list is always returned (copied from ``DEFAULT_SIZE_OPTIONS`` on the
        fallback paths) so callers can never mutate the module-level default.
        """
        param = request.env["ir.config_parameter"].sudo().get_param(OPTIONS_PARAM)
        if not param:
            return list(DEFAULT_SIZE_OPTIONS)
        options = [int(x.strip()) for x in param.split(",") if x.strip().isdigit()]
        return options or list(DEFAULT_SIZE_OPTIONS)

    def _prepare_portal_layout_values(self):
        """Add the page-size selector data to the portal layout values.

        Inject the whitelist of allowed page sizes and the currently active
        page size so the pager template can render the selector and keep the
        user's choice across pagination, sorting, filtering and searching.
        """
        values = super()._prepare_portal_layout_values()
        values.update(
            portal_pager_size_options=self._get_portal_pager_size_options(),
            portal_pager_size=self._items_per_page,
        )
        return values
