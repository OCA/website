# -*- coding: utf-8 -*-

from openerp import http
from openerp.http import request


class WebsiteCookieConsent(http.Controller):
    @http.route("/website_cookieconsent", type='json', auth="public")
    def get_config_cookie_config(self, **kw):
        cookie_config = request.env['ir.config_parameter'].sudo().get_param(
            'website.cookie_consent_config')
        return {'cookie_config': cookie_config}
