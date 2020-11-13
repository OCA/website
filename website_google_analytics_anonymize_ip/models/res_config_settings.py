# Copyright 2020 CodeNext
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    google_analytics_anonymize_ip = fields.Boolean(
        'Google Analytics Anonymize IP',
        related='website_id.google_analytics_anonymize_ip',
        readonly=False)
