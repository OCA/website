# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import werkzeug.urls

from odoo import models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def google_map_link(self, zoom=10):
        self.ensure_one()
        base_url = "https://www.openstreetmap.org"
        country = self.country_id or self.env.company.country_id
        lon, lat = self.partner_longitude, self.partner_latitude
        if lon and lat:
            return f"{base_url}/directions?from=&to={lat},{lon}#map={zoom}/{lat}/{lon}"
        else:
            params = {
                "query": f"{self.street or ''}, {self.city or ''} {self.zip or ''},"
                f" {country and country.display_name or ''}",
                "zoom": zoom,
            }
            return f"{base_url}/search?" + werkzeug.urls.url_encode(params)
