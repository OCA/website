# Copyright 2020 Advitus MB
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).
from pathlib import Path

from psycopg2 import OperationalError

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _dispatch(cls):
        res = super(IrHttp, cls)._dispatch()
        # if not website request - skip
        website = request.env["website"].sudo().get_current_website()
        if not website:
            return res

        # if it can't access the user_id,
        # it means that an exception has been
        # raised and the cursor is currently closed
        try:
            user = website.user_id
        except OperationalError:
            return res
        if request.uid == user.id:
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
                    return request.redirect("/web/login?redirect=%s" % path)
        return res
