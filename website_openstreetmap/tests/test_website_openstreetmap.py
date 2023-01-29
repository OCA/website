import urllib

from odoo.tests import common


class TestWebsite(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env["res.partner"]

        cls.partner_1 = Partner.create(
            {
                "name": "Onestein B.V.",
                "street": "Reduitlaan 45",
                "zip": "4814 DC",
                "city": "Breda",
                "country_id": cls.env.ref("base.nl").id,
            }
        )

    def test_01_openstreetmap_link(self):
        Partner = self.env["res.partner"]

        result = self.partner_1.openstreetmap_link(zoom=10)

        coordinates = Partner._geo_localize(
            street="Reduitlaan 45",
            zip="4814 DC",
            city="Breda",
            country="Netherlands",
        )
        str_address = self.env["base.geocoder"].geo_query_address(
            street="Reduitlaan 45",
            zip="4814 DC",
            city="Breda",
            country="Netherlands",
        )
        expected_result = "https://www.openstreetmap.org/search?%s#map=%s/%s/%s" % (
            urllib.parse.urlencode({"query": str_address}),
            10,
            coordinates[0],
            coordinates[1],
        )

        self.assertEqual(expected_result, result)
