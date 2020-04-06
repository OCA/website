# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2015 Antiun Ingeniería S.L. <http://antiun.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http


class CookieNotice(http.Controller):
    @http.route(
        "/website_cookie_notice/ok",
        auth="public",
        website=True,
        type="json",
        methods=["POST"],
    )
    def accept_cookies(self):
        """Stop spamming with cookie banner."""
        http.request.session["accepted_cookies"] = True
        http.request.env["ir.ui.view"].search([("type", "=", "qweb")]).clear_caches()
        return {"result": "ok"}
