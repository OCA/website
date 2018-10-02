# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import http
from openerp.http import request
from openerp.addons.website.controllers.main import Website


class Main(Website):
    @http.route()
    def index(self, **kw):
        return request.redirect('/web')
