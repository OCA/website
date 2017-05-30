# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import odoo.tests


class TestUi(odoo.tests.HttpCase):
    def test_01_demo_country_dropdown_tour(self):
        self.phantom_js(
            "/",
            "odoo.__DEBUG__.services['web_tour.tour']." +
            "run('website_snippet_country_dropdown_tour_demo_page')",
            "odoo.__DEBUG__.services['web_tour.tour']" +
            ".tours.website_snippet_country_dropdown_tour_demo_page.ready"
        )
