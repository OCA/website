# -*- coding: utf-8 -*-
##############################################################################
#
# Odoo, an open source suite of business apps
# This module copyright (C) 2015 bloopark systems (<http://bloopark.de>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.models import Model
from openerp import fields
from openerp.addons.web.http import request
import urlparse
import re


class Website(Model):

    """Adds the fields for CDN."""

    _inherit = 'website'

    DEFAULT_CDN_FILTERS = [
        "^/[^/]+/static/",
        "^/web/(css|js)/",
        "^/website/image/",
    ]

    cdn_activated = fields.Boolean('Activate CDN for assets', default=False)
    cdn_url = fields.Char('CDN Base URL', default="//localhost:8069/")
    cdn_filters = fields.Text(
        'CDN Filters',
        help="URL matching those filters will be rewritten using the CDN "
             "Base URL",
        default='\n'.join(DEFAULT_CDN_FILTERS))

    def get_cdn_url(self, cr, uid, uri, context=None):
        # Currently only usable in a website_enable request context
        if request and request.website and not request.debug:
            cdn_url = request.website.cdn_url
            cdn_filters = (request.website.cdn_filters or '').splitlines()
            for flt in cdn_filters:
                if flt and re.match(flt, uri):
                    return urlparse.urljoin(cdn_url, uri)
        return uri
