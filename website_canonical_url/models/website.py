# -*- coding: utf-8 -*-
##############################################################################
#
#    Authors: Thomas Rehn
#    Copyright (c) 2015 initOS GmbH & Co. KG (<http://www.initos.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp.osv import orm
from openerp.http import request


class website(orm.Model):
    _inherit = 'website'

    def get_canonical_urls(self, cr, uid, ids, req=None, **kwargs):
        canonical_urls = []
        if req is None:
            req = request.httprequest
        if req and req.base_url:
            canonical_urls.append(req.base_url)
        return canonical_urls
