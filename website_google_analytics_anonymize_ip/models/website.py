# Copyright 2020 CodeNext
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):

    _inherit = 'website'

    google_analytics_anonymize_ip = fields.Boolean(
        "Google Analytics Anonymize IP")
