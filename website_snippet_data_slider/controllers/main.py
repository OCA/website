# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import json
from openerp import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


import logging
_logger = logging.getLogger(__name__)


class Website(Website):

    @http.route(
        '/website/data_slider/<string:model>',
        type='http',
        auth='public',
        methods=['GET'],
        website=True,
    )
    def get_data_slider_data(self, model, **kwargs):
        # @TODO: Figure out a better way to hand the data to client
        # @TODO: Security eval on this - should be fine, model perms?
        # @TODO: Better exception handling (or any at all, really)
        res = []
        _logger.debug(kwargs)
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
