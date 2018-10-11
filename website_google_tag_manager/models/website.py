# Copyright 2016 ABF OSIELL <http://osiell.com>
# Copyright 2018 Tecnativa - Cristina Martin R.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    google_tag_manager_key = fields.Char("Container ID")
