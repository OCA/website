# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class WebsiteNoIndex(Website):
    @http.route(['/robots.txt'], type='http', auth="public")
    def robots(self):
        """Generate a robots.txt file from the controller endpoints."""
        values = {
            'url_root': request.httprequest.url_root,
        }

        endpoint_tree = request.env['ir.http'].get_endpoint_tree()
        access_rules = endpoint_tree.get_robots()

        values['access_rules'] = access_rules
        return request.render('website_no_index.robots', values,
                              mimetype='text/plain')
