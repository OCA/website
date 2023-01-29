import urllib

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def openstreetmap_link(self, zoom=15):
        coordinates = self._geo_localize(
            street=self.street or "",
            zip=self.zip or "",
            city=self.city or "",
            state=(self.state_id and self.state_id.name) or "",
            country=(self.country_id and self.country_id.name) or "",
        )
        str_address = self.env["base.geocoder"].geo_query_address(
            street=self.street or "",
            zip=self.zip or "",
            city=self.city or "",
            state=(self.state_id and self.state_id.name) or "",
            country=(self.country_id and self.country_id.name) or "",
        )
        return "https://www.openstreetmap.org/search?%s#map=%s/%s/%s" % (
            urllib.parse.urlencode({"query": str_address}),
            zoom,
            coordinates[0],
            coordinates[1],
        )
