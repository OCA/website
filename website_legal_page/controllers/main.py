# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website.controllers.main import Website


class Legal(Website):

    @http.route([
        '/legal/<string:page>',
    ],
        auth='public',
        type='http',
        website=True,
    )
    def show_legal_page(self, page, **kwargs):
        return self.page('website_legal_page.%s' % page, **kwargs)
