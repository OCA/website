# Copyright 2018 Camptocamp
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class Website(models.Model):
    _inherit = 'website'

    addthis_enabled = fields.Boolean("AddThis.com")
    addthis_pubid = fields.Char("Public ID")
    addthis_adv_config = fields.Text(
        'Advanced JS config', help='Add your custom JS settings.')
