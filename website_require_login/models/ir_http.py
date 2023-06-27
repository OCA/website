# Copyright 2020 Advitus MB
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
    def _check_require_auth(cls):
        # if not website request - skip
        website = request.env["website"].sudo().get_current_website()
        if not website:
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
        path = request.httprequest.path
        for auth_path in auth_paths:
            if auth_path == path or Path(auth_path) in Path(path).parents:
                redirect_path = "/web/login?redirect=%s" % path
                return request.redirect(redirect_path, code=302)
