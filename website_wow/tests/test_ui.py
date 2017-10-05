# -*- coding: utf-8 -*-
# Copyright 2017 LasLabs Inc.
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl)

from odoo.tests import HttpCase


class TestUi(HttpCase):

    post_install = True
    at_install = False

    def test_wow(self):
        tour_module = 'odoo.__DEBUG__.services["web_tour.tour"]'
        self.phantom_js(
            url_path='/page/contactus?debug=assets&enable_editor=1',
            code='%s.run("website_wow_editor")' % tour_module,
            ready='%s.tours.website_wow_editor.ready' % tour_module,
            login='admin',
        )
