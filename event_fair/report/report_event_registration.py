# -*- coding: utf-8 -*-
# © 2016 Antiun Ingeniería S.L. - Jairo Llopis
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models, tools


class EventRegistration(models.Model):
    _inherit = "report.event.registration"

    commercial_partner_id = fields.Many2one(
        "res.partner",
        "Commercial partner",
        readonly=True,
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

    def init(self, cr):
        """Initialize the sql view for the event registration."""
        # TODO Better inheritance mechanism than hardcoding all the view again
        # (when upstream does not hardcode themselves, of course)
        tools.drop_view_if_exists(cr, 'report_event_registration')

        # Mostly copied from core Odoo
        cr.execute("""CREATE VIEW report_event_registration AS (
            SELECT
                e.id::varchar || '/' || coalesce(r.id::varchar, '') AS id,
                e.id AS event_id,
                e.user_id AS user_id,
                r.user_id AS user_id_registration,
                r.name AS name_registration,
                e.company_id AS company_id,
                e.date_begin AS event_date,
                count(r.id) AS nbevent,
                sum(r.nb_register) AS nbregistration,
                CASE WHEN r.state IN ('draft')
                    THEN r.nb_register
                    ELSE 0 END AS draft_state,
                CASE WHEN r.state IN ('open','done')
                    THEN r.nb_register
                    ELSE 0 END AS confirm_state,
                e.type AS event_type,
                e.seats_max AS seats_max,
                e.state AS event_state,
                r.state AS registration_state,
                r.commercial_partner_id AS commercial_partner_id,
                r.square_meters AS square_meters,
                r.location_id AS location_id
            FROM
                event_event e
                LEFT JOIN event_registration r ON (e.id=r.event_id)

            GROUP BY
                event_id,
                user_id_registration,
                r.id,
                registration_state,
                r.nb_register,
                event_type,
                e.id,
                e.date_begin,
                e.user_id,
                event_state,
                e.company_id,
                e.seats_max,
                name_registration,
                r.commercial_partner_id,
                r.location_id
        )
        """)
