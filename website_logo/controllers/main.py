# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Antiun Ingenieria S.L. - Antonio Espinosa
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
##############################################################################

import functools
import logging
from cStringIO import StringIO

import openerp
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.modules import get_module_resource


db_monodb = http.db_monodb
_logger = logging.getLogger(__name__)


class Website(http.Controller):

    def _image_logo_get(self, cr, domain=None):
        if domain:
            cr.execute("""SELECT logo, write_date
                            FROM website
                           WHERE domain = %s
                       """, (domain,))
        else:
            cr.execute("""SELECT logo, write_date
                            FROM website
                       """)
        row = cr.fetchone()
        if row and row[0]:
            return StringIO(str(row[0]).decode('base64')), row[1]
        return False, False

    @http.route([
        '/web/binary/website_logo',
        '/website_logo',
        '/website_logo.png',
    ], type='http', auth="none", cors="*")
    def website_logo(self, dbname=None, **kw):
        imgname = 'website_nologo.png'
        placeholder = functools.partial(
            get_module_resource,
            'website_logo', 'static', 'src', 'img')
        uid = None
        if request.session.db:
            dbname = request.session.db
            uid = request.session.uid
        elif dbname is None:
            dbname = db_monodb()
        if not uid:
            uid = openerp.SUPERUSER_ID
        if uid and dbname:
            try:
                # create an empty registry
                registry = openerp.modules.registry.Registry(dbname)
                env = request.httprequest.environ
                domain = env.get('HTTP_HOST', '').split(':')[0]
                with registry.cursor() as cr:
                    image, mtime = self._image_logo_get(cr, domain)
                    if not image:
                        image, mtime = self._image_logo_get(cr, 'localhost')
                    if image:
                        response = http.send_file(
                            image, filename=imgname, mtime=mtime)
                        return response
            except Exception:  # pragma: no cover
                _logger.exception(openerp._(
                    'Could not get website logo, falling back to default',
                ))
        return http.send_file(placeholder(imgname))
