# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
import odoo.tests


class TestUi(odoo.tests.HttpCase):
    def test_01_demo_country_phone_code_dropdown_tour(self):
        self.start_tour(
            "/",
            "website_snippet_country_phone_code_dropdown_tour_demo_page",
            login="admin",
        )
