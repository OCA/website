# Copyright 2018 Onestein
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    # Replaces the web.base.url system parameter
    base_url = fields.Char(
        string='Base Url'
    )
