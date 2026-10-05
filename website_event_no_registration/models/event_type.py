# Copyright 2026 - Today: GRAP https://www.grap.coop
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class EventType(models.Model):
    _inherit = "event.type"

    registration_allowed = fields.Boolean(default=True)
