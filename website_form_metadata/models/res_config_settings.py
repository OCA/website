# -*- coding: utf-8 -*-
# Copyright 2018 David Vidal <david.vidal@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_form_enable_metadata = fields.Boolean(
        related="website_id.website_form_enable_metadata",
    )
