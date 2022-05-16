from odoo import http
from odoo.http import request
from odoo.tools import config

from odoo.addons.website.controllers.main import Website


class Website(Website):
    @http.route(["/robots.txt"], type="http", auth="public")
    def robots(self, **kwargs):

        return request.render(
            "website_no_crawler_environment.robots",
            {
                "url_root": request.httprequest.url_root,
                "server_env": config.options.get("running_env", False),
            },
            mimetype="text/plain",
        )
