# Copyright 2020 Alexandre Díaz - Tecnativa
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request


class WebsiteLegalPage(http.Controller):
    @http.route(["/shop/terms"], type="http", auth="public", website=True)
    def terms(self, **kw):
        """
        Ensure the website_legal_page template usage, even if the page was edited.
        This is done in this way because 'http.route' wins to
        'website.rewrite' 301 redirections.
        """
        return request.redirect("/legal")
