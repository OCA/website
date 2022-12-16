from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class Website(Website):
    @http.route(["/robots.txt"], type="http", auth="public")
    def robots(self, **kwargs):

        disable = (
            request.env["ir.config_parameter"]
            .sudo()
            .get_param("website.crawler.disable", False)
        )

        return request.render(
            "website_no_crawler.robots",
            {
                "url_root": request.httprequest.url_root,
                "disable": disable,
            },
            mimetype="text/plain",
        )
