# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
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

from odoo.addons.web.controllers.main import Binary
import odoo
from odoo import http
from odoo.http import request
from odoo.modules import get_resource_path
from cStringIO import StringIO
import functools


db_monodb = http.db_monodb


class WebsiteLogo(Binary):
    @http.route([
#        '/web/binary/website_logo',
        '/website_logo',
        '/website_logo.png',
    ], type='http', auth="none", cors="*", website=True)
    def website_logo(self, dbname=None, **kw):
        imgname = 'logo.png'
        uid = None
        placeholder = functools.partial(get_resource_path, 'web', 'static', 'src', 'img')
        if request.session.db:
            dbname = request.session.db
            uid = request.session.uid
        elif dbname is None:
            dbname = db_monodb()
        if not uid:
            uid = odoo.SUPERUSER_ID
        if uid and dbname:
            try:
                # create an empty registry
                registry = odoo.modules.registry.Registry(dbname)
                with registry.cursor() as cr:
                    cr.execute("""
                        SELECT c.website_logo, c.write_date
                        FROM res_users u
                        LEFT JOIN res_company c
                        ON c.id = u.company_id
                        WHERE u.id = %s
                    """, (uid,))
                    row = cr.fetchone()
                    if row and row[0]:
                        image_data = StringIO(str(row[0]).decode('base64'))
                        return http.send_file(image_data, filename=imgname, mtime=row[1])
            except Exception:
                pass
        return http.send_file(placeholder(imgname))
        # return super(WebsiteLogo, self).company_logo(dbname=dbname, **kw)
