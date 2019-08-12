# Copyright 2017 Simone Orsi.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    group_ids = fields.Many2many(
        comodel_name='res.groups',
    )
