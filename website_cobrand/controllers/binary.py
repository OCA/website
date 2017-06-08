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
from openerp.addons.web.controllers.main import Binary
from openerp.modules.registry import Registry
from openerp import http
import logging
from io import BytesIO


_logger = logging.getLogger(__name__)


class Binary(Binary):

    @http.route([
        '/web/binary/company_logo',
        '/logo',
        '/logo.png',
    ], type='http', auth="none", cors="*")
    def company_logo(self, dbname=None, **kw):
        '''
        Override company logo lookup to add a company lookup by URI if user is
            not logged in
        :param  dbname: str Name of DB
        :param  get_parent: bool Get the parent company's logo instead?
        '''
        sup = lambda: super(Binary, self).company_logo(dbname=dbname, **kw)
        imgname = 'logo.png'
        request = http.request
        company_mdl = request.env['res.company'].sudo()
        if request.session.db:
            if not request.session.uid:
                dbname = request.session.db
                host = request.httprequest.host_url
                company_id = company_mdl.find_by_website(
                    host
                )
                _logger.debug('Found for uri %s - %s', host, company_id)
                if len(company_id) > 1:
                    _logger.error(
                        'More than 1 company for URI %s. Using first result.',
                        host
                    )
                    company_id = company_id[0]
                elif len(company_id) == 0:
                    return sup()
                if kw.get('get_parent') and company_id.parent_id:
                    company_id = company_id.parent_id
                try:
                    # create an empty registry
                    registry = Registry(dbname)
                    with registry.cursor() as cr:
                        cr.execute("""SELECT c.logo_web, c.write_date
                                        FROM res_company c
                                       WHERE c.id = %s
                                   """, (company_id.id,))
                        row = cr.fetchone()
                        if row and row[0]:
                            image_data = BytesIO(str(row[0]).decode('base64'))
                            return http.send_file(
                                image_data, filename=imgname, mtime=row[1]
                            )
                        else:
                            return sup()
                except Exception as e:
                    _logger.error('Unable to get company logo - %s', e)
                    return sup()
        return sup()
