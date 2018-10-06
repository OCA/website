# -*- coding: utf-8 -*-
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleLegal(WebsiteSale):

    @http.route()
    def terms(self, **kw):
        return request.redirect('/legal/terms-of-use')
