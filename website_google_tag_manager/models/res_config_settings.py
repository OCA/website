# Copyright 2016 ABF OSIELL <http://osiell.com>
# Copyright 2018 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    google_tag_manager_key = fields.Char(
        'Container ID',
        related='website_id.google_tag_manager_key')
