# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
from openerp import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


class Website(Website):

    @http.route(
        '/website/field_autocomplete/<string:model>',
        type='http',
        auth='public',
        methods=['GET'],
        website=True,
    )
    def _get_autocomplete_data(self, model, **kwargs):
        res = []
        domain = json.loads(kwargs.get('domain', "[]"))
        fields = json.loads(kwargs.get('fields', "[]"))
        limit = kwargs.get('limit', None)
        if limit:
            limit = int(limit)
        for rec_id in request.env[model].search(domain, limit=limit):
            res.append({
                k: getattr(rec_id, k, None) for k in fields
            })
        return json.dumps(res)
