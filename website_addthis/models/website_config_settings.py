# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    addthis_enabled = fields.Boolean(related='website_id.addthis_enabled')
    addthis_pubid = fields.Char(related='website_id.addthis_pubid')
    addthis_adv_config = fields.Text(related='website_id.addthis_adv_config')
