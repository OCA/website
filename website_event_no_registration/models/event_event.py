# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    registration_allowed = fields.Boolean(
        copy=True, compute="_compute_registration_allowed", readonly=False, store=True
    )

    @api.depends("event_type_id")
    def _compute_registration_allowed(self):
        for event in self:
            if not event.event_type_id:
                event.registration_allowed = True
            else:
                event.registration_allowed = event.event_type_id.registration_allowed

    @api.depends(
        "date_tz",
        "event_registrations_started",
        "date_end",
        "seats_available",
        "seats_limited",
        "seats_max",
        "event_ticket_ids.sale_available",
        "registration_allowed",
    )
    def _compute_event_registrations_open(self):
        res = super(
            EventEvent, self.filtered(lambda x: x.registration_allowed)
        )._compute_event_registrations_open()
        for event in self.filtered(lambda x: not x.registration_allowed):
            event.event_registrations_open = False
        return res
