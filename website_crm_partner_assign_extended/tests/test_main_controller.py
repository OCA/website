# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests.common import HttpCase, tagged

from ..controllers.main import WebsiteCrmPartnerAssignCity


@tagged("post_install", "-at_install")
class TestWebsiteCrmPartnerAssignCity(HttpCase):
    def setUp(self):
        super(TestWebsiteCrmPartnerAssignCity, self).setUp()

    def test_sitemap_partners(self):
        rule = "/partners/"
        qs = ""
        results = list(WebsiteCrmPartnerAssignCity.sitemap_partners(self.env, rule, qs))
        self.assertEqual(len(results), 6)
        self.assertEqual(results[0]["loc"], "/partners")
        self.assertEqual(results[1]["loc"], "/partners/grade/bronze-4")
        self.assertEqual(results[2]["loc"], "/partners/grade/silver-3")

    def test_partners_by_state_and_city(self):

        partner = self.env.ref("base.res_partner_1")
        country = self.env["res.country"].create({"name": "test-country"})
        grade = self.env["res.partner.grade"].create({"name": "Test Grade"})
        state = self.env["res.country.state"].create(
            {"name": "Test State", "country_id": country.id, "code": "000"}
        )
        city = self.env["res.city"].create(
            {"name": "Test City", "country_id": country.id, "state_id": state.id}
        )
        partner.write(
            {
                "website_published": True,
                "country_id": country.id,
                "city_id": city.id,
                "city": False,
                "grade_id": grade.id,
            }
        )
        response = self.url_open(
            "/partners/grade/%s/country/%s/state/%s/city/%s"
            % (grade.id, country.id, state.id, city.id),
            headers={"Accept": "text/html"},
        )
        self.assertEqual(response.status_code, 200)
