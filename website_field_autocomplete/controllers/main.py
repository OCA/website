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
    def _get_field_autocomplete(self, model, **kwargs):
        """ Return json autocomplete data """
        domain = json.loads(kwargs.get('domain', "[]"))
        fields = json.loads(kwargs.get('fields', "[]"))
        limit = kwargs.get('limit', None)
        res = self._get_autocomplete_data(model, domain, fields, limit)
        return json.dumps(res.values())

    def _get_autocomplete_data(self, model, domain, fields, limit=None):
        """ Gets and returns raw record data
        Params:
            model: Model name to query on
            domain: Search domain
            fields: List of fields to get
            limit: Limit results to
        Returns:
            Dict of record dicts, keyed by ID
        """
        res = {}
        if limit:
            limit = int(limit)
        self.record_ids = request.env[model].search(domain, limit=limit)
        for rec_id in self.record_ids:
            res[rec_id.id] = {
                k: getattr(rec_id, k, None) for k in fields
            }
        return res
