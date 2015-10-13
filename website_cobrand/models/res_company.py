# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Dave Lasley <dave@laslabs.com>
#    Copyright: 2015 LasLabs, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, api
from urlparse import urlparse
import re


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def find_by_website(self, uri, ):
        '''
        Take in a URI, sanitize, search db, return results
        :param  uri: str Company URI
        :return company_ids: res.company
        '''
        uri = urlparse(uri)
        no_port = uri.netloc.split(':')[0]
        results = self.search([('website', '=ilike', '%%%s%%' % no_port)])
        validator = re.compile(r'^(\w+://)?(www.)?%s(:\d+)?(/.*)?' % no_port)
        company_ids = []
        for company_id in results:
            if validator.match(company_id.website):
                company_ids.append(company_id.id)
        return self.browse(company_ids)
