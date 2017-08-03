# -*- coding: utf-8 -*-
# Copyright 2016 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.http import request
from openerp.addons.website_field_autocomplete.controllers.main import Website


class WebsiteAutocomplete(Website):

    def _get_autocomplete_data(self, model, domain, fields, limit=None):
        """ Perform recursive search_reads to get all related data """
        res = super(WebsiteAutocomplete, self)._get_autocomplete_data(
            model, domain, fields, limit,
        )
        self.record_ids = request.env[model].search(domain)
        for field in filter(lambda f: '.' in f, fields):
            for rec_id in self.record_ids:
                res[rec_id.id][field] = self._get_relation_data(
                    rec_id, field,
                )
        return res

    def _get_relation_data(self, record_id, field_name):
        """ Iterate dot notated fields and inject data into object """
        obj = record_id
        for field_part in field_name.split('.'):
            obj = getattr(obj, field_part, None)
            if obj is None:
                return obj
        return obj
