# Copyright 2016-2017 LasLabs Inc.
# Copyright 2019 Simone Orsi - Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.http import request

from odoo.addons.website_form.controllers.main import WebsiteForm

import json


class WebsiteForm(WebsiteForm):

    @http.route(
        '/website/recaptcha/',
        type='http',
        auth='public',
        methods=['POST'],
        website=True,
        multilang=False,
    )
    def recaptcha_public(self):
        recaptcha_model = request.env['website.form.recaptcha'].sudo()
        creds = recaptcha_model._get_api_credentials(
            request.website,
        )
        return json.dumps({
            'site_key': creds['site_key']
        })

    def extract_data(self, model, values):
        """ Inject ReCaptcha validation into pre-existing data extraction """
        res = super(WebsiteForm, self).extract_data(model, values)
        if model.website_form_recaptcha:
            recaptcha_model = request.env['website.form.recaptcha'].sudo()
            recaptcha_model.validate_request(request, values)
        return res
