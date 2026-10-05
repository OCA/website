# Copyright 2024 Moduon Team S.L. <info@moduon.team>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).


from odoo.tests import TransactionCase


class TestModule(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_with_address = cls.env["res.partner"].create(
            {
                "name": "Demo OpenStreetMap Partner",
                "street": "3 Grande rue des feuillants",
                "city": "lyon",
                "zip": "69001",
                "country_id": cls.env.ref("base.fr").id,
            }
        )

    def test_with_lon_lat(self):
        self.partner_with_address.write(
            {
                "partner_longitude": 4.837005,
                "partner_latitude": 45.7702588,
            }
        )
        self.assertEqual(
            self.partner_with_address.google_map_link(zoom=15),
            "https://www.openstreetmap.org/directions?"
            "from=&to=45.7702588,4.837005#map=15/45.7702588/4.837005",
        )

    def test_with_address(self):
        self.assertEqual(
            self.partner_with_address.google_map_link(zoom=15),
            "https://www.openstreetmap.org/search?"
            "query=3+Grande+rue+des+feuillants%2C+lyon+69001%2C+France&zoom=15",
        )
