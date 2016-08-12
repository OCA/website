# -*- coding: utf-8 -*-
# Copyright 2015 Therp BV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import http, _


class Demo(http.Controller):
    @http.route('/website_backend_views/demo/', auth='user', website=True)
    def index(self, debug=False):
        if not http.request.env.ref(
                'website_backend_views.demo_index', raise_if_not_found=False):
            return _('You need to install this module in demo mode for this '
                     'url to work!')
        return http.request.render('website_backend_views.demo_index')
