# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
from odoo.tests.common import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestUi(HttpCase):
    def test_01_demo_country_dropdown_tour(self):
        self.start_tour(
            "/",
            "website_snippet_country_dropdown_tour_demo_page",
            login="admin",
        )
