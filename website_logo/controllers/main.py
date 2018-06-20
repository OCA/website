import functools
import logging
import io
import base64

from odoo import _, http, SUPERUSER_ID
from odoo.http import request
from odoo.modules import get_module_resource, registry

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
            return io.BytesIO(base64.b64decode(row[0])), row[1]
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
            uid = SUPERUSER_ID
        if uid and dbname:
            try:
                # create an empty registry
                reg = registry.Registry(dbname)
                env = request.httprequest.environ
                domain = env.get('HTTP_HOST', '').split(':')[0]
                with reg.cursor() as cr:
                    image, mtime = self._image_logo_get(cr, domain)
                    if not image:
                        image, mtime = self._image_logo_get(cr, 'localhost')
                    if image:
                        response = http.send_file(
                            image, filename=imgname, mtime=mtime)
                        return response
            except Exception:  # pragma: no cover
                _logger.exception(_(
                    'Could not get website logo, falling back to default',
                ))
        return http.send_file(placeholder(imgname))
