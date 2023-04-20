from odoo import http
from odoo.http import request

from odoo.addons.website.controllers.backend import WebsiteBackend


class WebsitePlausibleBackend(WebsiteBackend):
    @http.route("/website/fetch_dashboard_data", type="json", auth="user")
    def fetch_dashboard_data(self, website_id, date_from, date_to):
        res = super().fetch_dashboard_data(website_id, date_from, date_to)
        Website = request.env["website"]
        request.env.user.has_group("website.group_website_designer")
        current_website = (
            website_id and Website.browse(website_id) or Website.get_current_website()
        )
        res["dashboards"][
            "plausible_share_url"
        ] = current_website._get_plausible_share_url()
        return res
