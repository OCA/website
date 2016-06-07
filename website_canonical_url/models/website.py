# -*- coding: utf-8 -*-
# © initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.http import request


class website(models.Model):
    _inherit = 'website'

    @api.multi
    def get_canonical_url(self, req=None):
        canonical_url = None
        if req is None:
            req = request.httprequest
        if req and req.base_url:
            canonical_url = req.base_url
            print canonical_url
        return canonical_url
