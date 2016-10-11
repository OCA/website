# -*- coding: utf-8 -*-
# © initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api
from openerp.http import request
from urlparse import urlparse, urlunparse


class website(models.Model):
    _inherit = 'website'

    @api.multi
    def get_canonical_url(self, req=None):
        canonical_url = None
        if req is None:
            req = request
        if req and req.httprequest.path:
            lang = self.env.lang
            if lang == request.website.default_lang_code:
                canonical_url = req.httprequest.path
            else:
                url_parts = urlparse(req.httprequest.path)
                url_parts = list(url_parts)
                # change the path of the url
                url_parts[2] = lang + url_parts[2]
                canonical_url = urlunparse(url_parts)
        # Special case for rerouted requests to root path
        try:
            if (canonical_url.startswith("/page/") and
                    self.menu_id.child_id[0].url == canonical_url):
                canonical_url = "/"
        except:
            pass
        return canonical_url
