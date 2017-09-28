# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import HttpCase


class UICase(HttpCase):

    post_install = True
    at_install = False

    def test_website_snippet_barcode_editor(self):
        tour_module = 'odoo.__DEBUG__.services["web_tour.tour"]'
        self.phantom_js(
            url_path="/",
            code='%s.run("website_snippet_barcode")' % tour_module,
            ready='%s.tours.website_snippet_barcode.ready' % tour_module,
            login="admin",
        )
