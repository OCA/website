# -*- coding: utf-8 -*-
# © initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from urlparse import urlparse, urlunparse
from odoo import api, models
from odoo.http import request


class Website(models.Model):
    _inherit = 'website'

    @api.multi
    def get_canonical_url(self, req=None):
        """Construct and return both root and canonical url."""
        canonical_url = None
        root = None
        if req is None:  # pragma: no cover
            req = request
        if req and req.httprequest.path:
            lang = self.env.lang
            rel_path = req.httprequest.path
            root = request.httprequest.url_root
            if lang == request.website.default_lang_code:
                canonical_url = root[:-1] + rel_path
            else:
                url_parts = urlparse(req.httprequest.path)
                url_parts = list(url_parts)
                # change the path of the url
                url_parts[2] = lang + url_parts[2]
                canonical_url = root + urlunparse(url_parts)
        # Special case for rerouted requests to root path
        try:
            if (rel_path.startswith("/page/") and
                    self.menu_id.child_id[0].url == rel_path):
                canonical_url = root
        except:  # pragma: no cover
            pass
        return root[:-1], canonical_url
