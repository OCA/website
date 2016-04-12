# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class EventRegistration(models.Model):
    _inherit = "event.registration"

    square_meters = fields.Float(
        help="Amount of square meters reserved by this partner.",
    )
    location_id = fields.Many2one(
        "event.track.location",
        "Location",
        help="Location inside the fair (A1 stand, 3rd floor...).",
    )
