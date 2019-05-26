# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import json
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


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
        if limit:
            limit = int(limit)
        res = request.env[model].search_read(
            domain, fields, limit=limit
        )
        return {r['id']: r for r in res}
