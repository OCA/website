# -*- coding: utf-8 -*-
# © 2015 Agile Business Group sagl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import functools
from cStringIO import StringIO

import openerp
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.modules import get_module_resource

db_monodb = http.db_monodb


class Website(http.Controller):

    def _image_logo_get(self, cr, domain=None):
        if domain:
            cr.execute("""SELECT logo, write_date
                            FROM website
                           WHERE name = %s
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
        imgname = 'website_logo.png'
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
            except Exception:
                return http.send_file(placeholder(imgname))
        return http.send_file(placeholder(imgname))
