# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website.controllers.main import Website
from six import raise_from
from werkzeug.exceptions import NotFound


class Legal(Website):

    @http.route([
        '/legal/<string:page>',
    ],
        auth='public',
        type='http',
        website=True,
    )
    def show_legal_page(self, page, **kwargs):
        try:
            return self.page('website_legal_page.%s' % page, **kwargs)
        except ValueError as error:
            raise_from(NotFound, error)
