# Copyright 2020 Trey - Antonio González <antonio@trey.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    cookiebot_id = fields.Char(
        string='Cookiebot ID',
        help='This field holds the ID,'
        ' needed for Cookiebot functionality.',
    )
