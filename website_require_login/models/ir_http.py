# Copyright 2020 Advitus MB
# Copyright 2024 Simone Rubino - Aion Tech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from pathlib import Path

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls, endpoint):
        res = cls._check_require_auth()
        if res:
            return res
        return super()._dispatch(endpoint)

    @classmethod
    def _serve_fallback(cls):
        res = cls._check_require_auth()
        if res:
            return res
        return super()._serve_fallback()

    @classmethod
    def _require_login_whitelist_paths(cls):
        """List of paths that must always be available to all users."""
        return [
            # backend is already protected by login,
            # also /web/login, /web/assets, /web/image and others
            # are needed to correctly render the login page
            "/web",
            "/website/translations",
            "/jsonrpc",
            "/xmlrpc",
        ]

    @classmethod
    def _require_login_get_matching_path(cls, path, search_paths):
        """Return which one of `search_paths` is a parent of `path`."""
        path_inst = Path(path)
        for search_path in search_paths:
            if search_path == path or Path(search_path) in path_inst.parents:
                matching_path = search_path
                break
        else:
            matching_path = None
        return matching_path

    @classmethod
    def _check_require_auth(cls):
        # if not website request - skip
        website = request.env["website"].sudo().get_current_website()
        if not website:
            return None

        # Skip whitelisted paths
        path = request.httprequest.path
        whitelist_paths = cls._require_login_whitelist_paths()
        whitelist_path = cls._require_login_get_matching_path(path, whitelist_paths)
        if whitelist_path:
            return None

        if request.uid and (request.uid != website.user_id.id):
            return None
        auth_paths = (
            request.env["website.auth.url"]
            .sudo()
            .search(
                [
                    ("website_id", "=", website.id),
                ]
            )
            .mapped("path")
        )
        auth_path = cls._require_login_get_matching_path(path, auth_paths)
        if auth_path:
            redirect_path = "/web/login?redirect=%s" % path
            return request.redirect(redirect_path, code=302)
