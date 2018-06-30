# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl)

from odoo.tests import common, HttpCase


@common.at_install(False)
@common.post_install(True)
class TestUi(HttpCase):

    post_install = True
    at_install = False

    def test_wow(self):
        tour_module = 'odoo.__DEBUG__.services["web_tour.tour"]'
        self.phantom_js(
            url_path='/',
            code='%s.run("website_wow_tour_editor")' % tour_module,
            ready='%s.tours.website_wow_tour_editor.ready' % tour_module,
            login='admin',
        )
