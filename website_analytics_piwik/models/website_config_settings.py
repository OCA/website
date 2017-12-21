# Copyright 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    has_piwik_analytics = fields.Boolean(
        "Piwik Analytics",
        related=['website_id', 'has_piwik_analytics'])
    piwik_analytics_id = fields.Integer(
        related=['website_id', 'piwik_analytics_id'])
    piwik_analytics_host = fields.Char(
        related=['website_id', 'piwik_analytics_host'])
