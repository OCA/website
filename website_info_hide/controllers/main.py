from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class WebsiteInfo(Website):
    @http.route("/website/info", type="http", auth="public", website=True, sitemap=True)
    def website_info(self, **kwargs):
        return request.render("website.page_404")
