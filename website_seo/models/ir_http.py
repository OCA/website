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
from openerp import models
from openerp.http import request

import werkzeug


class IrHttp(models.TransientModel):
    _inherit = 'ir.http'

    def _find_handler(self, return_rule=False):
        """Update handler finding to avoid endless recursion."""
        handler = super(IrHttp, self)._find_handler(return_rule=return_rule)

        # ToDo: I reuse some parts of the _dispatch() function in
        # addons/website/models/ir_http.py, maybe we can re-structure
        # (complete overwrite) this function to have the needed values at this
        # place
        path = request.httprequest.path.split('/')

        request.website = request.registry['website'].get_current_website(
            request.cr, request.uid, context=request.context)

        langs = [lg[0] for lg in request.website.get_languages()]
        cook_lang = request.httprequest.cookies.get('website_lang')
        nearest_lang = self.get_nearest_lang(path[1])
        preferred_lang = ((cook_lang if cook_lang in langs else False)
                          or self.get_nearest_lang(request.lang)
                          or request.website.default_lang_code)

        request.lang = nearest_lang or preferred_lang

        # added handling from addons/website/models/ir_http.py in _dispatch()
        # function to avoid endless recursion when using different languages
        if (path[1] != request.website.default_lang_code
                and path[1] == request.lang):
            raise werkzeug.exceptions.NotFound()

        return handler
