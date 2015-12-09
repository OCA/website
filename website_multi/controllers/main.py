# -*- coding: utf-8 -*-
# © 2014 OpenERP SA
# © 2015 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

import werkzeug

from openerp.addons.web import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


class website_multi(Website):

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        cr, uid, context = request.cr, request.uid, request.context
        page = 'homepage'
        main_menu = request.website.menu_id
        first_menu = main_menu.child_id and main_menu.child_id[0]
        if first_menu:
            if not (first_menu.url.startswith(('/page/', '/?', '/#')) or (first_menu.url == '/')):
                return request.redirect(first_menu.url)
            if first_menu.url.startswith('/page/'):
                return request.registry['ir.http'].reroute(first_menu.url)
        return self.page(page)

    @http.route('/website/add/<path:path>', type='http', auth="user", website=True)
    def pagenew(self, path, noredirect=False, add_menu=None):
        cr, uid, context = request.cr, request.uid, request.context

        xml_id = request.registry['website'].new_page(request.cr, request.uid, path, context=request.context)
        if add_menu:
            request.registry['website.menu'].create(cr, uid, {
                'name': path,
                'url': '/page/' + xml_id,
                'parent_id': request.website.menu_id.id,
                'website_id': request.website.id
            }, context=context)

        # Reverse action in order to allow shortcut for /page/<website_xml_id>
        url = "/page/" + re.sub(r"^website\.", '', xml_id)

        if noredirect:
            return werkzeug.wrappers.Response(url, mimetype='text/plain')

        return werkzeug.utils.redirect(url)
