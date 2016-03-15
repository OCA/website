# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    commercial_partner_id = fields.Many2one(
        "res.partner",
        "Commercial partner",
        related="partner_id.commercial_partner_id",
        readonly=True,
        store=True,
        help="Commercial partner related to the chosen partner.",
    )
    square_meters = fields.Float(
        help="Amount of square meters reserved by this partner.",
    )
    location_id = fields.Many2one(
        "event.track.location",
        "Location",
        help="Location inside the fair (A1 stand, 3rd floor...).",
    )

    @api.model
    def _init_commercial_partner_id(self):
        """Force recalculation of related field."""
        for s in self.search([("partner_id", "!=", False),
                              ("commercial_partner_id", "=", False)]):
            # Stupid? Yes. Nevermind, it works.
            s.partner_id = s.partner_id
